import inspect
from argparse import Namespace
from typing import Any

from inspect import Parameter as _


def dispatch(namespace: Namespace, instance: Any = None) -> Any:
	"""Adapt an argparse.Namespace to a Python callable."""
	func = namespace.func
	if instance is not None:
		func = func.__get__(instance)

	parameters = inspect.signature(func).parameters
	values = vars(namespace).copy()
	values.pop("_command", None)
	values.pop("func", None)

	args: list[Any] = []
	kwargs: dict[str, Any] = {}

	for name, parameter in parameters.items():
		kind = parameter.kind
		if kind is _.POSITIONAL_ONLY and name in values:
			args.append(values.pop(name))
		elif kind is _.POSITIONAL_OR_KEYWORD and name in values:
			args.append(values.pop(name))
		elif kind is _.VAR_POSITIONAL:
			args.extend(values.pop(name, ()))
		elif kind is _.KEYWORD_ONLY and name in values:
			kwargs[name] = values.pop(name)
		elif kind is _.VAR_KEYWORD:
			kwargs.update(values)
			values.clear()

	kwargs.update(values)

	return func(*args, **kwargs)
