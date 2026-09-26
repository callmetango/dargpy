from argparse import Namespace

import pytest

from darg import Cli, flag, exclusive


def Given_exclusive_group_declarations():

	def When_flags_are_declared_in_an_exclusive_group():

		cli = Cli()

		with cli:
			with exclusive():
				flag("verbose")
				flag("quiet")

		def Then_only_one_flag_can_be_used():
			with pytest.raises(SystemExit):
				cli.parse_args(["--verbose", "--quiet"])

	def When_an_exclusive_group_is_not_required():

		cli = Cli()

		with cli:
			with exclusive():
				flag("verbose")
				flag("quiet")

		actual = cli.parse_args([])

		def Then_no_member_is_required():
			assert actual == Namespace(verbose=False, quiet=False)

	def When_an_exclusive_group_is_required():

		cli = Cli()

		with cli:
			with exclusive(required=True):
				flag("verbose")
				flag("quiet")

		def Then_one_member_is_required():
			with pytest.raises(SystemExit):
				cli.parse_args([])

	def When_declarations_follow_an_exclusive_group():

		cli = Cli()

		with cli:
			with exclusive():
				flag("verbose")

			flag("quiet")

		actual = cli.parse_args(["--quiet"])

		def Then_the_declaration_is_added_to_the_parser():
			assert actual == Namespace(verbose=False, quiet=True)

	def When_exclusive_groups_are_nested():

		cli = Cli()

		with cli:
			with exclusive():
				flag("verbose")

				with pytest.raises(RuntimeError, match="cannot be nested"):
					with exclusive():
						flag("quiet")
