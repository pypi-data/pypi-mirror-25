# coding=utf-8

# pylint: disable=redefined-outer-name,missing-docstring

import pytest
from django.template.exceptions import TemplateSyntaxError

from django_tag_parser.django_tag_parser import TagParser
from django_tag_parser_test.utils import MockParser, MockToken


@pytest.fixture
def example_parser():
  return TagParser(args=['foo'], kwargs=['bar'], opt_kwargs=['baz'])


def test_valid_parser(example_parser: TagParser):

  actual = example_parser.parse(MockParser(), MockToken(["1", "bar=2", "baz=3"])).resolve({})

  expected = {'bar': '2', 'baz': '3', 'foo': '1'}
  assert actual == expected


def test_missing_args(example_parser: TagParser):

  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken([]))


def test_missing_kwargs(example_parser: TagParser):

  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken(["1"]))


def test_invalid_order(example_parser: TagParser):
  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken(["baz=3", "1", "bar=2"]))


def test_duplicate(example_parser: TagParser):
  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken(["1", "bar=2", "bar=3"]))


def test_too_many_positional(example_parser: TagParser):
  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken(["1", "2", "3"]))


def test_unknown_tag(example_parser: TagParser):
  with pytest.raises(TemplateSyntaxError):
    example_parser.parse(MockParser(), MockToken(["1", "bar=2", "bazbar=3"])).resolve({})
