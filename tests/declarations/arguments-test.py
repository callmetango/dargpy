from argparse import Namespace

import pytest

from darg import Cli, Qualifier, Type, argument


def Given_argument_declarations():

	def When_a_qualifier_and_kwarg_specify_the_same_setting():

		cli = Cli()

		with cli:
			argument("value", Type(int), type=str)

		actual = cli.parse_args(["42"])

		def Then_the_qualifier_wins():
			assert actual == Namespace(value=42)

	def When_a_qualifier_and_kwarg_specify_different_settings():

		cli = Cli()

		with cli:
			argument("value", Type(int), metavar="VALUE")

		actual = cli.parse_args(["42"])

		def Then_both_settings_are_applied():
			assert actual == Namespace(value=42)

	def When_multiple_qualifiers_specify_the_same_setting():

		cli = Cli()

		with cli:
			argument("value", Qualifier(type=int), Qualifier(type=str))

		actual = cli.parse_args(["42"])

		def Then_the_last_qualifier_wins():
			assert actual == Namespace(value="42")

	def When_a_positional_argument_is_declared():

		cli = Cli()

		with cli:
			argument("value")

		actual = cli.parse_args(["hello"])

		def Then_the_name_is_used_as_the_destination():
			assert actual == Namespace(value="hello")

	def When_an_argument_has_an_explicit_none_default():

		cli = Cli()

		with cli:
			argument("value", default=None)

		actual = cli.parse_args(["value"])

		def Then_none_does_not_change_argument_parsing():
			assert actual == Namespace(value="value")

	def When_an_argument_uses_the_reserved_command_name():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					argument("_command")

	def When_an_argument_name_is_empty():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="name must not be empty"):
					argument("")

	def When_a_qualifier_uses_the_reserved_command_destination():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					argument("value", Qualifier(dest="_command"))


	def When_an_argument_uses_the_reserved_command_destination():

		cli = Cli()

		def Then_an_assertion_error_is_raised():
			with cli:
				with pytest.raises(AssertionError, match="reserved"):
					argument("value", dest="_command")

