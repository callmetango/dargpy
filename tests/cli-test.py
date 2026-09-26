import argparse

import pytest
from unittest.mock import Mock

from darg import Cli


# Configuration

def Given_cli_configuration():

	def When_no_parser_options_are_given():

		cli = Cli()

		def Then_argparse_defaults_are_used():
			assert cli.parser.add_help is True
			assert cli.parser.allow_abbrev is True
			assert cli.parser.argument_default is None
			assert cli.parser.conflict_handler == "error"
			assert cli.parser.exit_on_error is True
			assert cli.parser.formatter_class is argparse.HelpFormatter
			assert cli.parser.fromfile_prefix_chars is None
			assert cli.parser.prefix_chars == "-"
			assert cli.parser.epilog is None
			assert cli.parser.usage is None

	def When_all_parser_options_are_given():

		formatter = argparse.RawDescriptionHelpFormatter

		cli = Cli(
			name="darg",
			about="Test CLI",
			add_help=False,
			allow_abbrev=False,
			argument_default="DEFAULT",
			conflict_handler="resolve",
			epilog="EPILOG",
			exit_on_error=False,
			formatter_class=formatter,
			fromfile_prefix_chars="@",
			prefix_chars="+/",
			usage="darg [OPTIONS]",
		)

		def Then_all_options_are_forwarded_to_argparse():
			parser = cli.parser

			assert parser.prog == "darg"
			assert parser.description == "Test CLI"
			assert parser.add_help is False
			assert parser.allow_abbrev is False
			assert parser.argument_default == "DEFAULT"
			assert parser.conflict_handler == "resolve"
			assert parser.epilog == "EPILOG"
			assert parser.exit_on_error is False
			assert parser.formatter_class is formatter
			assert parser.fromfile_prefix_chars == "@"
			assert parser.prefix_chars == "+/"
			assert parser.usage == "darg [OPTIONS]"


# Context

def Given_an_active_cli_context():

	outer = Cli()
	inner = Cli()

	def When_another_cli_context_is_entered():

		try:
			with outer:
				with inner:
					pass
		except RuntimeError as error:
			actual = str(error)
		else:
			actual = None

		def Then_a_runtime_error_is_raised():
			assert actual == "Cli contexts cannot be nested"


# Argument parsing

def Given_a_cli():

	cli = Cli()
	parser = Mock()
	expected = argparse.Namespace()

	cli.parser = parser
	parser.parse_args.return_value = expected

	def When_arguments_are_parsed():

		arguments = ["--name", "Alice"]
		actual = cli.parse_args(arguments)

		def Then_the_arguments_are_forwarded_to_the_parser():
			parser.parse_args.assert_called_once_with(arguments)

		def Then_the_parser_result_is_returned():
			assert actual is expected


# Constructor validation

def Given_empty_prefix_characters():

	def When_the_cli_is_created():

		with pytest.raises(ValueError) as error:
			Cli(prefix_chars="")

		def Then_a_value_error_is_raised():
			assert str(error.value) == "prefix_chars must not be empty"


# Parent parsers

def Given_a_parent_parser():

	parent = argparse.ArgumentParser(add_help=False)
	parent.add_argument("--name")

	cli = Cli(parents=[parent])

	def When_the_parent_argument_is_parsed():

		actual = cli.parse_args(["--name", "Alice"])

		def Then_the_parent_argument_is_available():
			assert actual.name == "Alice"
