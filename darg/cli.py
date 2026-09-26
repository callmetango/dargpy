import argparse
from collections.abc import Sequence
from types import TracebackType
from typing import Any, Protocol, Self


class _ArgumentTarget(Protocol):
	def add_argument(self, *args: str, **kwargs: Any) -> Any:
		...


class Cli:
	"""Define a command-line interface using the darg DSL."""

	def __init__(
		self, name: str | None = None, about: str | None = None,
		parents: Sequence[argparse.ArgumentParser] | None = None,
		add_help: bool = True, allow_abbrev: bool = True,
		argument_default: Any = None, conflict_handler: str = "error",
		epilog: str | None = None, exit_on_error: bool = True,
		formatter_class: type[argparse.HelpFormatter] = argparse.HelpFormatter,
		fromfile_prefix_chars: str | None = None, prefix_chars: str = "-",
		usage: str | None = None, **kwargs: Any,
	) -> None:
		if not prefix_chars:
			raise ValueError("prefix_chars must not be empty")
		if parents is None:
			parents = []

		self.parser = argparse.ArgumentParser(
			prog=name, description=about, parents=parents, add_help=add_help,
			allow_abbrev=allow_abbrev, argument_default=argument_default,
			conflict_handler=conflict_handler, epilog=epilog,
			exit_on_error=exit_on_error, formatter_class=formatter_class,
			fromfile_prefix_chars=fromfile_prefix_chars, prefix_chars=prefix_chars,
			usage=usage, **kwargs,
		)

		self.add_help = add_help
		self.allow_abbrev = allow_abbrev
		self.argument_default = argument_default
		self.conflict_handler = conflict_handler
		self.exit_on_error = exit_on_error
		self.formatter_class = formatter_class
		self.fromfile_prefix_chars = fromfile_prefix_chars
		self.prefix_chars = prefix_chars
		self.prefix_char = prefix_chars[0]
		self.stack: list[_ArgumentTarget] = [self.parser]
		self.commands: list[str] = []
		self.subparsers: dict[argparse.ArgumentParser, Any] = {}
		self.exclusive = False

	def __enter__(self) -> Self:
		global _current

		if _current is not None:
			raise RuntimeError("Cli contexts cannot be nested")

		_current = self
		return self

	def __exit__(self, exc_type: type[BaseException] | None,
		exc_value: BaseException | None, traceback: TracebackType | None) -> None:
		global _current
		_current = None

	def parse_args(self, args: Sequence[str] | None = None) -> argparse.Namespace:
		return self.parser.parse_args(args)

	@property
	def current(self) -> _ArgumentTarget:
		return self.stack[-1]

	@property
	def command(self) -> str:
		return "/".join(self.commands)

	def push(self, parser: _ArgumentTarget, command: str) -> None:
		self.stack.append(parser)
		self.commands.append(command)

	def pop(self) -> None:
		self.stack.pop()
		self.commands.pop()


_current: Cli | None = None


def _cli() -> Cli:
	if _current is None:
		raise RuntimeError("DSL used outside a Cli context")
	return _current
