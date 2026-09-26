from argparse import ArgumentError, Namespace

import pytest

from darg import Cli, argument, command, flag, option


def Given_command_declarations():

	def When_a_nested_command_is_selected():

		cli = Cli()

		with cli:
			with command("release"):
				with command("upload"):
					argument("tag")

		actual = cli.parse_args(["release", "upload", "v1"])

		def Then_the_canonical_command_path_is_stored():
			assert actual._command == "release/upload"

	def When_a_command_is_defined_at_the_root():

		cli = Cli()

		with cli:
			with command("upload"):
				argument("tag")

		actual = cli.parse_args(["upload", "v1"])

		def Then_the_command_path_contains_only_the_command_name():
			assert actual._command == "upload"

	def When_custom_prefix_chars_are_used():

		cli = Cli(prefix_chars="+/")

		with cli:
			with command("upload"):
				flag("verbose", alias="v")

		actual = cli.parse_args(["upload", "++verbose"])

		def Then_the_prefix_character_is_inherited_by_the_command():
			assert actual == Namespace(_command="upload", verbose=True)

	def When_a_command_overrides_inherited_parser_configuration():

		cli = Cli(allow_abbrev=True)

		with cli:
			with command("upload", allow_abbrev=False):
				option("verbose")

		def Then_the_command_configuration_takes_precedence():
			with pytest.raises(SystemExit):
				cli.parse_args(["upload", "--verb", "value"])

	def When_a_command_description_is_given_as_a_kwarg():

		cli = Cli()

		with cli:
			with command("upload", description="kwargs"):
				argument("value")

		def Then_the_description_is_applied():
			assert cli.parser._actions[1].choices["upload"].description == "kwargs"

	def When_a_command_help_is_given_as_a_kwarg():

		cli = Cli()

		with cli:
			with command("upload", help="kwargs"):
				argument("value")

		def Then_the_help_is_applied():
			action = cli.parser._actions[1]
			assert action._choices_actions[0].help == "kwargs"

	def When_a_command_about_is_given():

		cli = Cli()

		with cli:
			with command("upload", about="DSL"):
				argument("value")

		def Then_about_is_applied_as_description_and_help():
			action = cli.parser._actions[1]
			child = action.choices["upload"]
			assert child.description == "DSL"
			assert action._choices_actions[0].help == "DSL"

	def When_a_command_about_overrides_a_description_kwarg():

		cli = Cli()

		with cli:
			with command("upload", about="DSL", description="kwargs"):
				argument("value")

		def Then_the_explicit_about_wins():
			assert cli.parser._actions[1].choices["upload"].description == "DSL"

	def When_a_command_name_is_declared_twice():

		cli = Cli()

		def Then_the_second_declaration_raises_an_argument_error():
			with cli:
				with command("upload"):
					pass

				with pytest.raises(ArgumentError):
					with command("upload"):
						pass

	def When_a_command_name_is_empty():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="name must not be empty"):
					with command(""):
						pass
