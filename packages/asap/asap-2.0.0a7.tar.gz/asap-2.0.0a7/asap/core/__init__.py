from . import api

import os
import sys
import threading
import subprocess
import logging
import pickle
import functools
import collections

FAIL_ON_MALFORMED_ACTIONS=False

def debug(msg):
  logging.debug(msg)

def warn(msg):
  logging.warning(msg)

class EventQueueImpl(api.EventQueue):
  def __init__(self):
    self.elements = []
    self.cv = threading.Condition()

  def append(self, event):
    try:
      self.cv.acquire()
      self.elements.append(event)
      api.EventQueue.append(self, event)
      self.cv.notify()
    finally:
      self.cv.release()

  def immediate(self, event):
    try:
      self.cv.acquire()
      self.elements.insert(0,event)
      api.EventQueue.immediate(self, event)
      self.cv.notify()
    finally:
      self.cv.release()

  def pop(self):
    try:
      self.cv.acquire()
      while len(self.elements) == 0:
        self.cv.wait()
      ret = self.elements.pop(0)
    finally:
      self.cv.release()
    return ret

  def __iter__(self):
    return iter(self.elements)

class FluentStorage(dict):
  def __init__(self, pairs=None):
    if pairs:
      assert(all([isinstance(p[0], api.Term) and isinstance(p[1], api.Term) for p in pairs]))
      dict.__init__(self, pairs)
    else:
      dict.__init__(self)
  def __getitem__(self,key):
    if not isinstance(key, api.Term):
      raise Exception("attempted to get fluent '{}' which is not an api.Term".format(repr(key)))
    return dict.__getitem__(self, key)
  def __setitem__(self,key,value):
    if not isinstance(key, api.Term) or not isinstance(value, api.Term):
      raise Exception("attempted to set fluent '{}' to value '{}' where at least one is not an api.Term".format(repr(key), repr(value)))
    return dict.__setitem__(self, key)
  def nice(self):
    return '\t'+'\n\t'.join([
      '{} => {}'.format(str(x[0]), str(x[1]))
      for x in self.items()])
  def load_from_file(self, filename):
    # empty this object
    self.clear()
    with open(filename, 'rb') as f:
      # update with k/v pairs from pickle
      self.update(pickle.load(f))
    
  def store_to_file(self, filename):
    # store items (k/v pairs) of this dict to pickle
    with open(filename, 'wb') as f:
      pickle.dump(list(self.items()), f)

def extractFluents(answerset):
  '''
  extract FluentStorage from an iterable of Term
  fluents are represented as val(FluentName,Timepoint,FluentValue) where we extract timepoint 0
  '''
  assert(all([isinstance(x,api.Term) for x in answerset]))
  #debug("extracting fluents from answer set {}".format(repr(answerset)))
  keyValuePairsNext = [ (t.args[0],t.args[2]) for t in answerset if t.pred == 'val' and t.args[1].pred == 0 ]
  return FluentStorage(keyValuePairsNext)

def sortActions(actions, answerset):
  class AnswersetRelationBasedComparator:
    def __init__(self, answerset):
      self.answerset = answerset
      # key = predicate, value = dict
      #   key = tuple(first action, first arguments)
      #   value = set of tuple(second action, second arguments)
      self.predcache = {}
    def update(self, pred):
      # extract full extension of predicate pred from answerset into self.predcache
      logging.debug("sortActions updating order "+repr(pred))
      if pred in self.predcache:
        return
      extracted = collections.defaultdict(set)
      # go over all non-reflexive atoms
      for atom in [ x for x in answerset if x.pred == pred and x.args[0] != x.args[1] ]:
        logging.debug("  "+str(atom))
        first, second = atom.args[0], atom.args[1]
        if __debug__:
          logging.debug("%s < %s", str(first), str(second))
        extracted[first].add(second)
      self.predcache[pred] = dict(extracted)
    def compare(self, first, second):
      # TODO 
      firstaction, firstpred = first
      secondaction, secondpred = second
      if __debug__:
        logging.debug("comparing %s and %s for order %s/%s", str(firstaction), str(secondaction), firstpred, secondpred)
      try:
        predc = self.predcache[firstpred]
        if __debug__:
          logging.debug("in cache for "+firstpred)
          for k, vv in predc.items():
            logging.debug("  %s <",str(k))
            for v in vv:
              logging.debug("    %s",str(v))
        ret = 0
        if secondaction in predc[firstaction]:
          ret = -1
        elif firstaction in predc[secondaction]:
          ret = 1
        if __debug__:
          logging.debug("comparing %s and %s yields %d", str(firstaction), str(secondaction), ret)
        return ret
      except KeyError:
        logging.warning("while sorting actions using order {}: could not compare {} and {}".format(
          firstpred, str(firstaction), str(secondaction)))
        return 0
    def __call__(self, first, second):
      cmp = lambda a, b: (a > b) - (a < b)
      # returns -1 if first < second
      # returns 0 if first and second are equal
      # returns 1 if first > second
      # integers for priorities are always first
      # other priorities are sorted by their predicate
      # and then by the relation encoded in the predicate
      pfirst, psecond = first[1], second[1]
      if isinstance(pfirst, int):
        if isinstance(psecond,int):
          # int/int
          ret = cmp(pfirst, psecond)
        else:
          # int/str
          ret = -1
      elif isinstance(psecond, int):
        # str/int
        ret = 1
      else:
        # str/str
        c = cmp(pfirst, psecond)
        if c != 0:
          # different predicates
          ret = c
        else:
          # same predicate -> look at answer set
          self.update(pfirst)
          ret = self.compare(first, second)
      return ret

  arbcmp = AnswersetRelationBasedComparator(answerset)
  logging.debug("actions before sorting: %s", repr(actions))
  s = sorted(actions, key=functools.cmp_to_key(arbcmp))
  logging.info("actions after sorting: %s", repr(s))
  return s

def extractActions(answerset):
  '''
  extract sequence of actions from an iterable of Term
  actions are represented as terms action(<actionname>(<arguments>),<priority>)
  output of this function is a sequence of tuples (<actionname>(<arguments>),<priority>)
  '''
  assert(all([isinstance(x,api.Term) for x in answerset]))
  actions = [ (t.args[0], t.args[1].pred) for t in answerset if t.pred == 'action' ]
  # now sort actions (either from given integer priority or using relation encoded in answer set)
  ret = sortActions(actions, answerset)
  #debug('\n  '.join(["extracted action schedule:"] + map(lambda x: '{}/{}/{}'.format(*x), ret)))
  return ret

def malformedAction(name, args, msg):
  message = "malformed action '{}' with arguments '{}' ({})".format(name, args, msg)
  if FAIL_ON_MALFORMED_ACTIONS:
    raise Exception(message)
  else:
    warn(message + " (ignoring)")

def executeActionSchedule(doApis, actions, environment, answerset, actionSchedule):
  """
  doApis is obtained from asap.core.separateApis() [first element]
  actions is obtained from asap.core.actionsFromApis() [first element]
  environment is an environment
  answerset is the answer set
  actionSchedule is obtained via asap.core.extractActions()
  """
  for d in doApis:
    d.beforeExecution()
  for name_args, prio in actionSchedule:
    name, args = name_args.pred, name_args.args
    if name not in actions:
      debug("known actions: "+repr(actions.keys()))
      malformedAction(name, args, 'unknown action')
      continue
    a = actions[name]
    in_arity, in_arity_mandatory = a.interface[1:]
    if len(args) < in_arity_mandatory or len(args) > in_arity:
      malformedAction(name, args, 'wrong number of arguments')
      continue
    inp = api.ActionInput(environment, args, answerset)
    #debug("executing action '{}' with arguments '{}'".format(name, args))
    a.execute(inp)
  for d in doApis:
    d.afterExecution()

def separateApis(pl):
  logging.info("separateApis got {} plugins: {}".format(len(pl), repr(pl)))
  doApis = [x for x in pl if isinstance(x,api.DoAPI)]
  eventApis = [x for x in pl if isinstance(x,api.EventAPI)]
  externalApis = [x for x in pl if isinstance(x,api.ExternalAPI)]
  logging.info("separateApis found doApis {} eventApis {} externalApis {}".format(repr(doApis), repr(eventApis), repr(externalApis)))
  return doApis, eventApis, externalApis

def registerQueue(eventApis, eq):
  for api in eventApis:
    api.setQueue(eq)

def actionsFromApis(doApis):
  actions = {}
  for api in doApis:
    for action in api.actions():
      name = action.interface[0]
      if name in actions:
        raise Exception("duplicate action '{}' registered: {} vs. {}".format(name, repr(actions[name].interface), repr(action.interface)))
      actions[name] = action
  return actions

def externalsFromApis(externalApis):
  externals = {}
  for api in externalApis:
    for external in api.externals():
      name = external.interface[0]
      if name in externals:
        raise Exception("duplicate external '{}' registered: {} vs. {}".format(name, repr(externals[name].interface), repr(external.interface)))
      externals[name] = external
  return externals

def rewrite(program, target):
  '''
  rewrite ASAP program for one of the supported targets
  '''
  assert(target in ['hex', 'clasp'])
  rewriterpath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'ASAP-Rewriter.jar')
  logging.info("rewriting program with target '{}':".format(target))
  if __debug__:
    logging.debug("ORIGINAL:")
    for o in program.split('\n'):
      logging.debug('OR '+o.strip('\n'))
  p = subprocess.Popen('java -jar {} -target={}'.format(rewriterpath, target),
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
  out, err = p.communicate(bytes(program, 'utf-8'))
  out = out.decode('utf-8')
  if len(out) == 0:
    # TODO make better error management
    raise Exception("no output from rewriter!")
  if __debug__:
    logging.debug("REWRITTEN:")
    for o in out.split('\n'):
      logging.debug('RW '+o.strip('\n'))
  return out
