from contextlib import contextmanager
from typing import Any, Iterator

from .cli import _cli
from .qualifiers import Qualifier


class _Undefined:
	def __repr__(self) -> str:
		return "UNDEFINED"


_UNDEFINED = _Undefined()


# Parser options inherited by commands.
_parser_defaults = (
	"add_help",
	"allow_abbrev",
	"argument_default",
	"conflict_handler",
	"exit_on_error",
	"formatter_class",
	"fromfile_prefix_chars",
	"prefix_chars",
)


def _kwargs(qualifiers: tuple[Qualifier, ...]) -> dict[str, Any]:
	kwargs: dict[str, Any] = {}

	for qualifier in qualifiers:
		if not isinstance(qualifier, Qualifier):
			raise TypeError(f"Unknown DSL qualifier: {qualifier!r}")
		kwargs.update(qualifier.kwargs)

	return kwargs


def _names(name: str, alias: str | None = None, *, prefix_char: str) -> list[str]:
	assert name, "name must not be empty"
	assert alias is None or alias, "alias must not be empty"

	pref = prefix_char if len(name) == 1 else prefix_char * 2
	names = [f"{pref}{name}"]

	if alias is not None:
		pref = prefix_char if len(alias) == 1 else prefix_char * 2
		names.append(f"{pref}{alias}")

	return names


def argument(name: str, *qualifiers: Qualifier, about: str | None = None,
		hint: str | None = None, default: Any = _UNDEFINED, dest: str | None = None,
		**kwargs: Any) -> None:
	"""Declare a positional command-line argument."""

	assert name, "name must not be empty"
	assert name != "_command", "_command is reserved by the DSL"
	assert dest != "_command", "_command is reserved by the DSL"

	qualifier_kwargs = _kwargs(qualifiers)
	assert qualifier_kwargs.get("dest") != "_command", "_command is reserved by the DSL"

	kwargs.update(qualifier_kwargs)

	if about is not None:
		kwargs["help"] = about
	if hint is not None:
		kwargs["metavar"] = hint
	if default is not _UNDEFINED:
		kwargs["default"] = default
	if dest is not None:
		kwargs["dest"] = dest

	assert kwargs.get("dest") != "_command", "_command is reserved by the DSL"

	_cli().current.add_argument(name, **kwargs)


def flag(name: str, *, alias: str | None = None, about: str | None = None,
		default: Any = _UNDEFINED, dest: str | None = None, **kwargs: Any) -> None:
	"""Declare a boolean command-line flag."""

	assert name, "name must not be empty"
	assert name != "_command", "_command is reserved by the DSL"
	assert alias is None or alias, "alias must not be empty"
	assert "action" not in kwargs, "action is controlled by flag()"
	assert dest != "_command", "_command is reserved by the DSL"
	assert kwargs.get("dest") != "_command", "_command is reserved by the DSL"

	if about is not None:
		kwargs["help"] = about
	if default is not _UNDEFINED:
		kwargs["default"] = default
	if dest is not None:
		kwargs["dest"] = dest

	kwargs["action"] = "store_true"

	cli = _cli()
	cli.current.add_argument(*_names(name, alias, prefix_char=cli.prefix_char), **kwargs)


def option(name: str, *qualifiers: Qualifier, alias: str | None = None,
		about: str | None = None, hint: str | None = None, default: Any = _UNDEFINED,
		dest: str | None = None, **kwargs: Any) -> None:
	"""Declare a named command-line option."""

	assert name, "name must not be empty"
	assert name != "_command", "_command is reserved by the DSL"
	assert alias is None or alias, "alias must not be empty"
	assert dest != "_command", "_command is reserved by the DSL"
	assert kwargs.get("dest") != "_command", "_command is reserved by the DSL"

	qualifier_kwargs = _kwargs(qualifiers)
	assert qualifier_kwargs.get("dest") != "_command", "_command is reserved by the DSL"

	kwargs.update(qualifier_kwargs)

	if about is not None:
		kwargs["help"] = about
	if hint is not None:
		kwargs["metavar"] = hint
	if default is not _UNDEFINED:
		kwargs["default"] = default
	if dest is not None:
		kwargs["dest"] = dest

	cli = _cli()
	cli.current.add_argument(*_names(name, alias, prefix_char=cli.prefix_char), **kwargs)


@contextmanager
def command(name: str, *, about: str | None = None, **kwargs: Any) -> Iterator[None]:
	"""Define a command."""

	assert name, "name must not be empty"
	assert "/" not in name, "command name must not contain '/'"

	cli = _cli()
	parser = cli.current

	subparsers = cli.subparsers.get(parser)

	if subparsers is None:
		subparsers = parser.add_subparsers()
		cli.subparsers[parser] = subparsers

	parser_kwargs = {key: getattr(cli, key) for key in _parser_defaults}
	parser_kwargs.update(kwargs)

	if about is not None:
		parser_kwargs["description"] = about
		parser_kwargs["help"] = about

	child = subparsers.add_parser(name, **parser_kwargs)
	cmdname = f"{cli.command}/{name}" if cli.command else name
	child.set_defaults(_command=cmdname)

	cli.push(child, name)

	try:
		yield
	finally:
		cli.pop()


@contextmanager
def exclusive(*, required: bool = False) -> Iterator[None]:
	"""Define a mutually exclusive group of arguments."""

	cli = _cli()

	if cli.exclusive:
		raise RuntimeError("Mutually exclusive groups cannot be nested")

	group = cli.current.add_mutually_exclusive_group(required=required)
	cli.stack.append(group)
	cli.exclusive = True

	try:
		yield
	finally:
		cli.exclusive = False
		cli.stack.pop()


@contextmanager
def group(name: str, *, about: str | None = None) -> Iterator[None]:
	"""Group arguments in help output."""

	assert name, "name must not be empty"

	cli = _cli()
	group = cli.current.add_argument_group(name, description=about)

	cli.stack.append(group)

	try:
		yield
	finally:
		cli.stack.pop()

