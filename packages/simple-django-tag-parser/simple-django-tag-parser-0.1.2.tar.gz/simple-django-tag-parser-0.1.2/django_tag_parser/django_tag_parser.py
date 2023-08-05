# coding=utf-8
"""Helper for parsing tags."""

import typing


from django.template.base import FilterExpression, token_kwargs
from django.template.exceptions import TemplateSyntaxError


class ParsedArguments(object):
  """Represents parsed arguments."""

  def __init__(self, parameters: typing.Mapping[str, FilterExpression]):
    self.parameters = parameters

  def resolve(self, context) -> typing.Mapping[str, object]:
    """Resolves all arguments and returns dict with these arguments."""
    return {
      k: v.resolve(context)
      for k, v in self.parameters.items()
    }


class TagParser(object):
  """Tag parser."""

  def __init__(
      self,
      args: typing.List[str],
      kwargs: typing.List[str]=tuple(),
      opt_kwargs: typing.Sequence[str]=tuple()
  ):
    """
    Creates this tag parser.

    :param args: List of all positional arguments name. Positional arguments are required.
    :param kwargs: List of required keyword argument names.
    :param opt_kwargs: List of optional keyword argument names

    After parsing all arguments will be available in a dictionary **by name**.

    """
    self.args = args
    self.kwargs = kwargs
    self.opt_kwargs = opt_kwargs

  def parse(self, parser, token) -> ParsedArguments:
    """Parse this tag"""
    return _Parser(
      args=list(self.args),
      kwargs=list(self.kwargs),
      opt_kwargs=list(self.opt_kwargs),
    ).parse(parser, token)


class _Parser(object):
  """

  This objects keeps state, hence it is not thread-safe.

  It is used in TagParser which is thread safe.
  """

  def __init__(
      self,
      args: typing.List[str],
      kwargs: typing.List[str]=tuple(),
      opt_kwargs: typing.Sequence[str]=tuple()
  ):
    self.name = None
    self.args = args
    self.kwargs = set(kwargs)
    self.opt_kwargs = set(opt_kwargs)
    self.all_kwargs = set()
    self.all_kwargs.update(self.opt_kwargs)
    self.all_kwargs.update(self.kwargs)
    self.unparsed_args = list(args)
    """
    Unparsed positional args.
    """
    self.result = {}

  def parse(self, parser, token) -> ParsedArguments:
    """Do parsing."""
    bits = token.split_contents()
    self.name = bits.pop(0)
    for bit in bits:
      self.parse_bit(parser, bit)
    self.finish_parsing()
    return ParsedArguments(self.result)

  def parse_bit(self, parser, bit):
    """Pares one bit (or token)"""
    kwarg = token_kwargs([bit], parser)
    if kwarg:
      self.parse_as_kwarg(kwarg)
    else:
      self.parse_as_positional_args(parser.compile_filter(bit))

  def parse_as_kwarg(self, kwarg):
    """Parse token we know is a kwarg."""
    if self.unparsed_args:
      raise TemplateSyntaxError(self.__KWARGS_BEFORE_KW.format(self.name, self.unparsed_args))
    param_name, expression = kwarg.popitem()
    if param_name in self.result:
      raise TemplateSyntaxError(self.__DUPLICATED_ARG.format(self.name, param_name))
    if param_name not in self.all_kwargs:
      raise TemplateSyntaxError(self.__UNKNOWN_KWARGS.format(self.name, param_name))
    self.result[param_name] = expression

  def parse_as_positional_args(self, expression):
    """Parse token that is a positional argument."""
    if not self.unparsed_args:
      raise TemplateSyntaxError(
        self.__TOO_MANY_POSITIONAL_ARGS.format(self.name, self.unparsed_args)
      )
    param_name = self.unparsed_args.pop(0)
    self.result[param_name] = expression

  def finish_parsing(self):
    """Checks on finish parsing."""
    if self.unparsed_args:
      raise TemplateSyntaxError(
        self.__TOO_MANY_POSITIONAL_ARGS.format(self.name, self.unparsed_args)
      )
    all_args = self.result.keys()
    required_kwargs = set(self.kwargs)
    missing = required_kwargs - all_args
    if missing:
      raise TemplateSyntaxError(
        self.__MISSING_KWARGS.format(self.name, missing)
      )

  __KWARGS_BEFORE_KW = (
    "Tag {} got keyword arguments while there are unparesed positional arguments {}"
  )
  __DUPLICATED_ARG = "Tag {} got duplicate argument: {}"
  __TOO_MANY_POSITIONAL_ARGS = "Tag {} has extra positional args: {}"
  __MISSING_POSITIONAL_ARGS = "Tag {} has positional args unfilled: {}"
  __MISSING_KWARGS = "Tag {} has missing positional args {}"
  __UNKNOWN_KWARGS = "Tag {} has unknown keyword argument {}"

