import logging.config
from functools import reduce


__all__ = 'configure', 'resolve'


class Configurator(logging.config.BaseConfigurator):

  def __init__(self, config):
    self.config = ConvertingDict(config)
    self.config.configurator = self

  def convert(self, value):
    if isinstance(value, dict):
      if not isinstance(value, ConvertingDict):
        value = ConvertingDict(value)
        value.configurator = self
      if '()' in value:
        value = self.configure_custom(value)

    return super(Configurator, self).convert(value)


class ConvertingDict(logging.config.ConvertingDict):
  '''Allows the use of custom factories when iterating configuration dictionaries'''

  def items(self):
    for key in dict.keys(self):
      value = self.get(key)
      if isinstance(value, dict):
        # force conversion on this level, may need to more general improvement
        for k, v in value.items():
          self.convert_with_key(k, v)

      yield key, self.convert_with_key(key, value)


def merge(target, source):
  '''Deep ``dict`` merge'''

  result = target.copy()  # shallow copy
  stack  = [(result, source)]
  while stack:
    currentTarget, currentSource = stack.pop()
    for key in currentSource:
      if key not in currentTarget:
        currentTarget[key] = currentSource[key]  # appending
      else:
        if isinstance(currentTarget[key], dict) and isinstance(currentSource[key], dict):
          currentTarget[key] = currentTarget[key].copy()  # nested dict copy
          stack.append((currentTarget[key], currentSource[key]))
        elif currentTarget[key] is not None and currentSource[key] is None:
          del currentTarget[key]  # remove key marked as None
        else:
          currentTarget[key] = currentSource[key]  # overriding

  return result


def configure(*args):
  '''Merged nested configuration dictionary is wrapped into a resolver'''

  merged = reduce(merge, args)
  return Configurator(merged).config


resolve = logging.config._resolve

