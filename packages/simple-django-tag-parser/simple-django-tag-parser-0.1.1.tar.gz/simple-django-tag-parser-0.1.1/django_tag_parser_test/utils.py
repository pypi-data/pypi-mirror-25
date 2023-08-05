# coding=utf-8

# pylint: disable=redefined-outer-name,missing-docstring,unused-argument,no-self-use

import typing


class MockToken(object):

  def __init__(self, tokens: typing.Sequence, name: str = "tag"):
    self.tokens = [name] + list(tokens)

  def split_contents(self):
    return list(self.tokens)


class MockFilterExpression(object):

  def __init__(self, value):
    self.value = value

  def resolve(self, ctx):
    return self.value

  def __str__(self):
    return self.value

  def __repr__(self):
    return self.value

  def __hash__(self) -> int:
    return hash(self.value)

  def __eq__(self, o: object) -> bool:
    return self.value == o.value


class MockParser(object):

  def compile_filter(self, value):
    return MockFilterExpression(value)
