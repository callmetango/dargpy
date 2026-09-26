from argparse import ArgumentError, Namespace

import pytest

from darg import Cli, Qualifier, flag, option


def Given_option_and_flag_declarations():

	def When_an_option_is_declared_twice_with_the_default_conflict_handler():

		cli = Cli()

		with cli:
			option("verbose")

			with pytest.raises(ArgumentError):
				option("verbose")

	def When_an_option_is_declared_twice_with_resolve_conflict_handler():

		cli = Cli(conflict_handler="resolve")

		with cli:
			option("verbose", default="first")
			option("verbose", default="second")

		actual = cli.parse_args([])

		def Then_the_later_declaration_is_used():
			assert actual == Namespace(verbose="second")

	def When_two_options_share_an_alias_with_the_default_conflict_handler():

		cli = Cli()

		with cli:
			option("verbose", alias="v")

			with pytest.raises(ArgumentError):
				option("version", alias="v")

	def When_a_flag_action_is_given_as_a_kwarg():

		cli = Cli()

		with cli:
			with pytest.raises(AssertionError):
				flag("verbose", action="store_false")

	def When_a_flag_has_an_explicit_default():

		cli = Cli()

		with cli:
			flag("verbose", default=True)

		actual = cli.parse_args([])

		def Then_the_explicit_default_is_used():
			assert actual == Namespace(verbose=True)

	def When_a_flag_has_an_alias_with_custom_prefix_chars():

		cli = Cli(prefix_chars="+/")

		with cli:
			flag("verbose", alias="v")

		actual = cli.parse_args(["+v"])

		def Then_the_alias_uses_the_configured_prefix():
			assert actual == Namespace(verbose=True)

	def When_an_option_has_no_default():

		cli = Cli()

		with cli:
			option("value")

		actual = cli.parse_args([])

		def Then_argparse_provides_the_default():
			assert actual == Namespace(value=None)

	def When_an_option_has_an_explicit_none_default():

		cli = Cli()

		with cli:
			option("value", default=None)

		actual = cli.parse_args([])

		def Then_none_is_used_as_the_default():
			assert actual == Namespace(value=None)

	def When_a_flag_has_an_explicit_none_default():

		cli = Cli()

		with cli:
			flag("verbose", default=None)

		actual = cli.parse_args([])

		def Then_none_is_used_as_the_default():
			assert actual == Namespace(verbose=None)

	def When_an_option_name_matches_another_option_alias():

		cli = Cli()

		with cli:
			option("verbose", alias="v")

			with pytest.raises(ArgumentError):
				option("v")

	def When_an_explicit_option_parameter_overrides_a_qualifier():

		cli = Cli()

		with cli:
			option("value", Qualifier(default="qualifier"), default="explicit")

		actual = cli.parse_args([])

		def Then_the_explicit_parameter_wins():
			assert actual == Namespace(value="explicit")

	def When_an_option_uses_the_reserved_command_name():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					option("_command")

	def When_an_option_name_is_empty():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="name must not be empty"):
					option("")

	def When_a_flag_uses_the_reserved_command_name():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					flag("_command")

	def When_a_flag_name_is_empty():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="name must not be empty"):
					flag("")

	def When_a_qualifier_uses_the_reserved_command_destination():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					option("value", Qualifier(dest="_command"))


	def When_an_option_uses_the_reserved_command_destination():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					option("value", dest="_command")

