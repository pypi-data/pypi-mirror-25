# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from contextlib import contextmanager
from optparse import OptionParser
from tempfile import NamedTemporaryFile

from pex.bin.pex import build_pex, configure_clp, configure_clp_pex_resolution
from pex.compatibility import to_bytes
from pex.fetcher import PyPIFetcher
from pex.package import SourcePackage, WheelPackage
from pex.resolver_options import ResolverOptionsBuilder
from pex.sorter import Sorter


@contextmanager
def parser_pair():
  builder = ResolverOptionsBuilder()
  parser = OptionParser()
  yield builder, parser


def test_clp_no_pypi_option():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)
    assert len(builder._fetchers) == 1
    options, _ = parser.parse_args(args=['--no-pypi'])
    assert len(builder._fetchers) == 0, '--no-pypi should remove fetchers.'
    assert options.repos == builder._fetchers


def test_clp_pypi_option_duplicate():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)
    assert len(builder._fetchers) == 1
    options, _ = parser.parse_args(args=['--pypi'])
    assert len(builder._fetchers) == 1
    assert options.repos == builder._fetchers


# TODO(wickman) We should probably add fetchers in order.
def test_clp_repo_option():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)
    assert len(builder._fetchers) == 1
    options, _ = parser.parse_args(args=['-f', 'http://www.example.com'])
    assert len(builder._fetchers) == 2
    assert builder._fetchers == options.repos


def test_clp_index_option():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)
    assert len(builder._fetchers) == 1
    options, _ = parser.parse_args(args=['-i', 'http://www.example.com'])
    assert len(builder._fetchers) == 2
    assert builder._fetchers == options.repos
    assert builder._fetchers[1] == PyPIFetcher('http://www.example.com')


def test_clp_build_precedence():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)
    assert builder._precedence == Sorter.DEFAULT_PACKAGE_PRECEDENCE

    parser.parse_args(args=['--no-build'])
    assert SourcePackage not in builder._precedence
    parser.parse_args(args=['--build'])
    assert SourcePackage in builder._precedence

    options, _ = parser.parse_args(args=['--no-wheel'])
    assert WheelPackage not in builder._precedence
    assert not options.use_wheel

    options, _ = parser.parse_args(args=['--wheel'])
    assert WheelPackage in builder._precedence
    assert options.use_wheel


# Make sure that we're doing append and not replace
def test_clp_requirements_txt():
  parser, builder = configure_clp()
  options, _ = parser.parse_args(args='-r requirements1.txt -r requirements2.txt'.split())
  assert options.requirement_files == ['requirements1.txt', 'requirements2.txt']


def test_clp_constraints_txt():
  parser, builder = configure_clp()
  options, _ = parser.parse_args(args='--constraint requirements1.txt'.split())
  assert options.constraint_files == ['requirements1.txt']


def test_clp_preamble_file():
  with NamedTemporaryFile() as tmpfile:
    tmpfile.write(to_bytes('print "foo!"'))
    tmpfile.flush()

    parser, resolver_options_builder = configure_clp()
    options, reqs = parser.parse_args(args=['--preamble-file', tmpfile.name])
    assert options.preamble_file == tmpfile.name

    pex_builder = build_pex(reqs, options, resolver_options_builder)
    assert pex_builder._preamble == to_bytes('print "foo!"')


def test_clp_prereleases():
  with parser_pair() as (builder, parser):
    configure_clp_pex_resolution(parser, builder)

    options, _ = parser.parse_args(args=[])
    assert not builder._allow_prereleases

    options, _ = parser.parse_args(args=['--no-pre'])
    assert not builder._allow_prereleases

    options, _ = parser.parse_args(args=['--pre'])
    assert builder._allow_prereleases
