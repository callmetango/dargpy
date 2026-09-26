from argparse import Namespace

from darg import Cli, command, group, option


def Given_argument_group_declarations():

	def When_options_are_declared_in_a_group():

		cli = Cli()

		with cli:
			with group("Authentication"):
				option("username")
				option("password")

		actual = cli.parser.format_help()

		def Then_the_options_appear_under_the_group_heading():
			assert "Authentication:" in actual
			assert "--username" in actual
			assert "--password" in actual

	def When_declarations_follow_a_group():

		cli = Cli()

		with cli:
			with group("Authentication"):
				option("username")

			option("verbose")

		actual = cli.parse_args(["--username", "alice", "--verbose", "yes"])

		def Then_the_declaration_is_added_to_the_parent_parser():
			assert actual == Namespace(username="alice", verbose="yes")

	def When_a_group_has_an_about():

		cli = Cli()

		with cli:
			with group("Authentication", about="Login credentials"):
				option("username")

		actual = cli.parser.format_help()

		def Then_the_about_is_used_as_the_group_description():
			assert "Authentication:" in actual
			assert "Login credentials" in actual

	def When_a_group_is_declared_inside_a_command():

		cli = Cli()

		with cli:
			with command("upload"):
				with group("Authentication"):
					option("username")

		actual = cli.parse_args(["upload", "--username", "alice"])

		def Then_the_option_belongs_to_the_command():
			assert actual == Namespace(_command="upload", username="alice")
