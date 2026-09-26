from typing import Any, Callable


class Qualifier:
	"""Qualify argparse configuration for a DSL declaration."""

	def __init__(self, **kwargs: Any) -> None:
		self.kwargs: dict[str, Any] = kwargs


class Choices(Qualifier):
	"""Restrict an argument to a set of values.

	Example::

		argument("format", Choices("json", "yaml"))
	"""

	def __init__(self, *values: Any) -> None:
		if not values:
			raise ValueError("at least one choice is required")
		super().__init__(choices=values)


class Type(Qualifier):
	"""Convert an argument value using a callable.

	Example::

		argument("port", Type(int))
	"""

	def __init__(self, converter: Callable[..., Any]) -> None:
		if not callable(converter):
			raise TypeError("converter must be callable")
		super().__init__(type=converter)


class Value(Qualifier):
	"""Store a constant value when an option is used.

	Example::

		option("mode", Value("fast"))
	"""

	def __init__(self, value: Any) -> None:
		super().__init__(action="store_const", const=value)


class _AppendValue(Qualifier):
	def __init__(self) -> None:
		super().__init__(action="append")

	def __call__(self, value: Any) -> Qualifier:
		return Qualifier(action="append_const", const=value)


AppendValue = _AppendValue()
Count = Qualifier(action="count")
OneOrMore = Qualifier(nargs="+")
Optional = Qualifier(nargs="?")
Required = Qualifier(required=True)
ZeroOrMore = Qualifier(nargs="*")

