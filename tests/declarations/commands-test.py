from argparse import ArgumentError

import pytest

from darg import Cli, argument, command, option


def commandParser(cli, *path):
	parser = cli.parser

	for name in path:
		parser = cli.subparsers[parser].choices[name]

	return parser


# Commands

def Given_a_CLI_with_an_upload_command():

	COMMAND = "upload"

	cli = Cli()

	with cli:
		with command(COMMAND):
			pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_command_path_is_stored():
			assert actual.get_default("_command") == COMMAND


def Given_a_CLI_with_a_nested_upload_command():

	PARENT = "release"
	COMMAND = "upload"
	PATH = f"{PARENT}/{COMMAND}"

	cli = Cli()

	with cli:
		with command(PARENT):
			with command(COMMAND):
				pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, PARENT, COMMAND)

		def Then_the_full_command_path_is_stored():
			assert actual.get_default("_command") == PATH


def Given_a_CLI_with_an_upload_command_and_a_function():

	COMMAND = "upload"

	def _upload(tag):
		return tag

	cli = Cli()

	with cli:
		with command(COMMAND, func=_upload):
			pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_command_function_is_stored():
			assert actual.get_default("func") is _upload


def Given_a_CLI_with_a_nested_upload_command_and_a_function():

	PARENT = "release"
	COMMAND = "upload"

	def _upload(tag):
		return tag

	cli = Cli()

	with cli:
		with command(PARENT):
			with command(COMMAND, func=_upload):
				pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, PARENT, COMMAND)

		def Then_the_command_function_is_stored():
			assert actual.get_default("func") is _upload


def Given_a_CLI_with_an_upload_command_and_an_argument():

	COMMAND = "upload"
	ARGUMENT = "tag"

	cli = Cli()

	with cli:
		with command(COMMAND):
			argument(ARGUMENT)

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_argument_is_declared():
			assert ARGUMENT in actual.format_usage()


def Given_a_CLI_with_an_upload_command_and_an_option():

	COMMAND = "upload"
	OPTION = "verbose"

	cli = Cli()

	with cli:
		with command(COMMAND):
			option(OPTION)

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_option_is_declared():
			assert f"--{OPTION}" in actual.format_help()


# Configuration

def Given_a_CLI_with_parser_configuration():

	COMMAND = "upload"

	cli = Cli(allow_abbrev=True)

	with cli:
		with command(COMMAND, allow_abbrev=False):
			pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_command_configuration_is_used():
			assert actual.allow_abbrev is False


def Given_a_CLI_with_an_upload_command_and_about():

	COMMAND = "upload"
	ABOUT = "Upload files"

	cli = Cli()

	with cli:
		with command(COMMAND, about=ABOUT):
			pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_the_command_description_is_about():
			assert actual.description == ABOUT


def Given_a_CLI_with_an_upload_command_and_help():

	COMMAND = "upload"
	HELP = "Upload files"

	cli = Cli()

	with cli:
		with command(COMMAND, help=HELP):
			pass

	def When_the_command_help_is_formatted():

		actual = cli.parser.format_help()

		def Then_the_help_is_used():
			assert HELP in actual


def Given_a_CLI_with_an_upload_command_and_about_and_description():

	COMMAND = "upload"
	ABOUT = "DSL"
	DESCRIPTION = "argparse"

	cli = Cli()

	with cli:
		with command(COMMAND, about=ABOUT, description=DESCRIPTION):
			pass

	def When_the_command_parser_is_retrieved():

		actual = commandParser(cli, COMMAND)

		def Then_about_has_precedence():
			assert actual.description == ABOUT


# Validation

def Given_a_CLI():

	EMPTY_NAME = ""
	NAME_WITH_SLASH = "release/upload"
	COMMAND = "upload"

	cli = Cli()

	def When_a_command_name_is_empty():

		with pytest.raises(AssertionError, match="name must not be empty") as error:
			with cli:
				with command(EMPTY_NAME):
					pass

		def Then_an_assertion_error_is_raised():
			assert error.type is AssertionError


	def When_a_command_name_contains_a_separator():

		with pytest.raises(AssertionError, match="must not contain '/'") as error:
			with cli:
				with command(NAME_WITH_SLASH):
					pass

		def Then_an_assertion_error_is_raised():
			assert error.type is AssertionError


	def When_the_same_command_is_declared_again():

		with cli:
			with command(COMMAND):
				pass

			with pytest.raises(ArgumentError) as error:
				with command(COMMAND):
					pass

		def Then_an_argument_error_is_raised():
			assert error.type is ArgumentError
