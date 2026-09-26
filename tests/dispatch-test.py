from argparse import Namespace
from typing import Any

import pytest

from darg import dispatch


# ---------------------------------------------------------------------------
# Basic dispatch
# ---------------------------------------------------------------------------

def Given_a_function_without_parameters():

	RESULT = "called"

	def _function() -> str:
		return RESULT

	namespace = Namespace(func=_function)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_function_is_called_without_arguments():
			assert actual == RESULT


def Given_a_function_that_returns_a_value():

	RESULT = object()

	def _function() -> object:
		return RESULT

	namespace = Namespace(func=_function)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_function_result_is_returned():
			assert actual is RESULT


def Given_a_non_callable_object():

	OBJECT = object()

	namespace = Namespace(func=OBJECT)

	def When_the_object_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_object_as_not_callable():
			assert error.type is TypeError


# ---------------------------------------------------------------------------
# Parameter names and ordering
# ---------------------------------------------------------------------------

def Given_an_argument_with_a_different_name_from_the_parameter():

	ARGUMENT_NAME = "Alice"

	def _function(name: str) -> str:
		return name

	namespace = Namespace(
		func=_function,
		other_name=ARGUMENT_NAME,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_parameter():
			assert error.type is TypeError


def Given_positional_arguments_in_a_different_namespace_order():

	ARGUMENTS = {
		"first": "Alice",
		"second": 42,
	}

	def _function(first: str, second: int, /) -> tuple[str, int]:
		return first, second

	namespace = Namespace(
		func=_function,
		second=ARGUMENTS["second"],
		first=ARGUMENTS["first"],
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_arguments_are_passed_in_parameter_order():
			assert actual == (
				ARGUMENTS["first"],
				ARGUMENTS["second"],
			)

		def Then_the_arguments_are_not_passed_in_namespace_order():
			assert actual != (
				ARGUMENTS["second"],
				ARGUMENTS["first"],
			)


# ---------------------------------------------------------------------------
# Positional-only parameters
# ---------------------------------------------------------------------------

def Given_a_missing_positional_only_argument():

	AGE = 42

	def _function(name: str, age: int, /) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		age=AGE,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_argument():
			assert error.type is TypeError


def Given_a_function_with_only_positional_only_parameters():

	NAME = "Alice"
	AGE = 42

	def _function(name: str, age: int, /) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		name=NAME,
		age=AGE,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_positional_arguments_are_passed():
			assert actual == (NAME, AGE)


def Given_a_positional_only_argument_with_a_default():

	DEFAULT_NAME = "Alice"

	def _function(name: str = DEFAULT_NAME, /) -> str:
		return name

	namespace = Namespace(func=_function)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_python_uses_the_default_argument():
			assert actual == DEFAULT_NAME


def Given_an_explicit_positional_only_argument_with_a_default():

	DEFAULT_NAME = "Alice"
	NAME = "Bob"

	def _function(name: str = DEFAULT_NAME, /) -> str:
		return name

	namespace = Namespace(
		func=_function,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_python_uses_the_explicit_argument():
			assert actual == NAME

		def Then_python_does_not_use_the_default_argument():
			assert actual != DEFAULT_NAME


def Given_a_missing_positional_only_argument_with_variable_keyword_arguments():

	REMAINING_ARGUMENTS = {
		"age": 42,
	}

	def _function(
		name: str,
		/,
		**arguments: Any,
	) -> tuple[str, dict[str, Any]]:
		return name, arguments

	namespace = Namespace(
		func=_function,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_positional_argument():
			assert error.type is TypeError


def Given_a_positional_only_argument_and_variable_keyword_arguments():

	NAME = "Alice"
	REMAINING_ARGUMENTS = {
		"age": 42,
	}

	def _function(
		name: str,
		/,
		**arguments: Any,
	) -> tuple[str, dict[str, Any]]:
		return name, arguments

	namespace = Namespace(
		func=_function,
		name=NAME,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_positional_argument_is_passed_separately():
			assert actual[0] == NAME

		def Then_the_positional_argument_is_not_passed_as_a_keyword_argument():
			assert actual[1] == REMAINING_ARGUMENTS


# ---------------------------------------------------------------------------
# Positional-or-keyword parameters
# ---------------------------------------------------------------------------

def Given_a_function_with_a_missing_required_argument():

	NAME = "Alice"

	def _function(name: str, age: int) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_parameter():
			assert error.type is TypeError


def Given_a_function_with_a_default_argument():

	NAME = "Alice"
	DEFAULT_AGE = 42

	def _function(
		name: str,
		age: int = DEFAULT_AGE,
	) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_python_uses_the_default_argument():
			assert actual == (NAME, DEFAULT_AGE)


def Given_an_explicit_argument_for_a_default_parameter():

	NAME = "Alice"
	DEFAULT_AGE = 42
	AGE = 23

	def _function(
		name: str,
		age: int = DEFAULT_AGE,
	) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		name=NAME,
		age=AGE,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_python_uses_the_explicit_argument():
			assert actual == (NAME, AGE)

		def Then_python_does_not_use_the_default_argument():
			assert actual != (NAME, DEFAULT_AGE)


# ---------------------------------------------------------------------------
# Keyword-only parameters
# ---------------------------------------------------------------------------

def Given_a_missing_keyword_only_argument():

	NAME = "Alice"

	def _function(
		*,
		name: str,
		enabled: bool,
	) -> tuple[str, bool]:
		return name, enabled

	namespace = Namespace(
		func=_function,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_argument():
			assert error.type is TypeError


def Given_a_function_with_only_keyword_only_parameters():

	NAME = "Alice"
	AGE = 42

	def _function(
		*,
		name: str,
		age: int,
	) -> tuple[str, int]:
		return name, age

	namespace = Namespace(
		func=_function,
		name=NAME,
		age=AGE,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_keyword_only_arguments_are_passed():
			assert actual == (NAME, AGE)


def Given_an_explicit_keyword_only_argument():

	ENABLED = True

	def _function(*, enabled: bool) -> bool:
		return enabled

	namespace = Namespace(
		func=_function,
		enabled=ENABLED,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_keyword_only_argument_is_passed():
			assert actual is ENABLED


def Given_a_falsy_keyword_only_argument():

	ENABLED = False

	def _function(*, enabled: bool) -> bool:
		return enabled

	namespace = Namespace(
		func=_function,
		enabled=ENABLED,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_keyword_only_argument_is_passed():
			assert actual is ENABLED


def Given_a_function_with_a_default_keyword_only_argument():

	NAME = "Alice"
	DEFAULT_ENABLED = True

	def _function(
		name: str,
		*,
		enabled: bool = DEFAULT_ENABLED,
	) -> tuple[str, bool]:
		return name, enabled

	namespace = Namespace(
		func=_function,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_python_uses_the_default_keyword_only_argument():
			assert actual == (NAME, DEFAULT_ENABLED)


def Given_a_keyword_only_argument_and_variable_keyword_arguments():

	ENABLED = True
	REMAINING_ARGUMENTS = {
		"name": "Alice",
		"age": 42,
	}

	def _function(
		*,
		enabled: bool,
		**arguments: Any,
	) -> tuple[bool, dict[str, Any]]:
		return enabled, arguments

	namespace = Namespace(
		func=_function,
		enabled=ENABLED,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_keyword_only_argument_is_passed_to_its_parameter():
			assert actual[0] is ENABLED

		def Then_the_keyword_only_argument_is_not_passed_as_a_remaining_argument():
			assert actual[1] == REMAINING_ARGUMENTS


# ---------------------------------------------------------------------------
# *args
# ---------------------------------------------------------------------------

def Given_multiple_arguments_for_a_variable_positional_parameter():

	ARGUMENTS = ("Alice", 42)

	def _function(*arguments: Any) -> tuple[Any, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_arguments_are_expanded():
			assert actual == ARGUMENTS

		def Then_the_arguments_are_not_passed_as_one_argument():
			assert actual != (ARGUMENTS,)


def Given_a_positional_or_keyword_argument_before_variable_positional_arguments():

	NAME = "Alice"
	ARGUMENTS = (42, 23)

	def _function(
		name: str,
		*arguments: int,
	) -> tuple[str, tuple[int, ...]]:
		return name, arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
		name=NAME,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_named_argument_is_passed_before_the_variable_arguments():
			assert actual == (
				NAME,
				ARGUMENTS,
			)


def Given_no_namespace_value_for_variable_positional_arguments():

	REMAINING_ARGUMENTS = {
		"name": "Alice",
	}

	def _function(
		*arguments: Any,
		**keyword_arguments: Any,
	) -> tuple[tuple[Any, ...], dict[str, Any]]:
		return arguments, keyword_arguments

	namespace = Namespace(
		func=_function,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_no_positional_arguments_are_passed():
			assert actual[0] == ()

		def Then_the_remaining_arguments_are_passed_as_keywords():
			assert actual[1] == REMAINING_ARGUMENTS


def Given_no_variable_positional_arguments():

	ARGUMENTS = ()

	def _function(*arguments: Any) -> tuple[Any, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_no_arguments_are_passed():
			assert actual == ARGUMENTS


def Given_a_named_argument_and_variable_positional_arguments():

	NAME = "Alice"
	ARGUMENTS = (42, 23)

	def _function(
		name: str,
		*arguments: int,
	) -> tuple[str, tuple[int, ...]]:
		return name, arguments

	namespace = Namespace(
		func=_function,
		name=NAME,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_named_argument_is_passed_to_its_parameter():
			assert actual[0] == NAME

		def Then_the_variable_positional_arguments_are_expanded():
			assert actual[1] == ARGUMENTS


def Given_falsy_variable_positional_arguments():

	ARGUMENTS = (0, False, "")

	def _function(*arguments: Any) -> tuple[Any, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_arguments_are_passed_unchanged():
			assert actual == ARGUMENTS


def Given_variable_positional_arguments_with_order():

	ARGUMENTS = ("first", "second", "third")

	def _function(*arguments: str) -> tuple[str, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_argument_order_is_preserved():
			assert actual == ARGUMENTS


def Given_variable_positional_and_keyword_only_arguments():

	POSITIONAL_ARGUMENTS = ("Alice", 42)
	ENABLED = True

	def _function(
		*arguments: Any,
		enabled: bool,
	) -> tuple[tuple[Any, ...], bool]:
		return arguments, enabled

	namespace = Namespace(
		func=_function,
		arguments=POSITIONAL_ARGUMENTS,
		enabled=ENABLED,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_variable_positional_arguments_are_expanded():
			assert actual[0] == POSITIONAL_ARGUMENTS

		def Then_the_keyword_only_argument_is_passed():
			assert actual[1] is ENABLED


# ---------------------------------------------------------------------------
# **kwargs
# ---------------------------------------------------------------------------

def Given_multiple_named_arguments_for_a_variable_keyword_parameter():

	ARGUMENTS = {
		"name": "Alice",
		"age": 42,
	}

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		**ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_named_arguments_are_expanded():
			assert actual == ARGUMENTS

		def Then_the_arguments_are_not_passed_as_one_mapping():
			assert actual != {"arguments": ARGUMENTS}


def Given_no_remaining_arguments_for_variable_keyword_arguments():

	POSITIONAL_ARGUMENT = "Alice"

	def _function(
		name: str,
		**arguments: Any,
	) -> tuple[str, dict[str, Any]]:
		return name, arguments

	namespace = Namespace(
		func=_function,
		name=POSITIONAL_ARGUMENT,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_named_argument_is_passed():
			assert actual[0] == POSITIONAL_ARGUMENT

		def Then_no_remaining_arguments_are_passed():
			assert actual[1] == {}


def Given_an_explicit_default_argument_and_variable_keyword_arguments():

	DEFAULT_AGE = 42
	AGE = 23
	REMAINING_ARGUMENTS = {
		"name": "Alice",
	}

	def _function(
		age: int = DEFAULT_AGE,
		**arguments: Any,
	) -> tuple[int, dict[str, Any]]:
		return age, arguments

	namespace = Namespace(
		func=_function,
		age=AGE,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_explicit_argument_is_passed():
			assert actual[0] == AGE

		def Then_the_default_argument_is_not_used():
			assert actual[0] != DEFAULT_AGE

		def Then_the_remaining_arguments_are_passed():
			assert actual[1] == REMAINING_ARGUMENTS


def Given_falsy_remaining_arguments():

	REMAINING_ARGUMENTS = {
		"enabled": False,
		"count": 0,
		"name": "",
		"value": None,
	}

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_arguments_are_passed_unchanged():
			assert actual == REMAINING_ARGUMENTS


def Given_arbitrary_remaining_arguments():

	REMAINING_ARGUMENTS = {
		"name": "Alice",
		"age": 42,
		"enabled": True,
	}

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_all_remaining_arguments_are_passed():
			assert actual == REMAINING_ARGUMENTS


def Given_a_namespace_with_only_a_command_for_a_variable_keyword_function():

	COMMAND = "greet"

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		_command=COMMAND,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_no_arguments_are_passed():
			assert actual == {}


# ---------------------------------------------------------------------------
# Remaining arguments and Python rejection
# ---------------------------------------------------------------------------

def Given_an_argument_without_a_matching_parameter():

	NAME = "Alice"
	UNEXPECTED_ARGUMENT = 42

	def _function(name: str) -> str:
		return name

	namespace = Namespace(
		func=_function,
		name=NAME,
		unexpected=UNEXPECTED_ARGUMENT,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_unexpected_argument():
			assert error.type is TypeError


# ---------------------------------------------------------------------------
# _command metadata
# ---------------------------------------------------------------------------

def Given_a_namespace_with_a_command_value():

	NAME = "Alice"
	COMMAND = "greet"

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		name=NAME,
		_command=COMMAND,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_command_is_not_passed_as_an_argument():
			assert actual == {
				"name": NAME,
			}


def Given_a_command_for_a_function_without_arguments():

	COMMAND = "greet"

	def _function() -> str:
		return COMMAND

	namespace = Namespace(
		func=_function,
		_command=COMMAND,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_function_is_called_without_arguments():
			assert actual == COMMAND


def Given_an_argument_named_like_internal_metadata():

	ARGUMENT = "Alice"

	def _function(_name: str) -> str:
		return _name

	namespace = Namespace(
		func=_function,
		_name=ARGUMENT,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_argument_is_passed():
			assert actual == ARGUMENT


def Given_a_function_with_a_command_parameter():

	COMMAND = "greet"

	def _function(_command: str) -> str:
		return _command

	namespace = Namespace(
		func=_function,
		_command=COMMAND,
	)

	def When_the_function_is_dispatched():

		with pytest.raises(TypeError) as error:
			dispatch(namespace)

		def Then_python_rejects_the_missing_parameter():
			assert error.type is TypeError


def Given_a_command_with_variable_positional_arguments():

	COMMAND = "greet"
	ARGUMENTS = ("Alice", 42)

	def _function(*arguments: Any) -> tuple[Any, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
		_command=COMMAND,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_variable_positional_arguments_are_passed():
			assert actual == ARGUMENTS


def Given_a_command_with_remaining_keyword_arguments():

	COMMAND = "greet"
	REMAINING_ARGUMENTS = {
		"name": "Alice",
		"age": 42,
	}

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		_command=COMMAND,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_remaining_arguments_are_passed():
			assert actual == REMAINING_ARGUMENTS


# ---------------------------------------------------------------------------
# Argument presence and falsy values
# ---------------------------------------------------------------------------

def Given_a_false_argument():

	ARGUMENT = False

	def _function(value: bool) -> bool:
		return value

	namespace = Namespace(
		func=_function,
		value=ARGUMENT,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_argument_is_passed():
			assert actual is ARGUMENT


def Given_falsy_values_for_all_argument_kinds():

	POSITIONAL_ONLY_ARGUMENT = 0
	POSITIONAL_OR_KEYWORD_ARGUMENT = False
	VARIABLE_POSITIONAL_ARGUMENTS = ("", 0)
	KEYWORD_ONLY_ARGUMENT = None
	REMAINING_ARGUMENTS = {
		"extra": False,
	}

	def _function(
		first: int,
		second: bool,
		/,
		*arguments: Any,
		enabled: Any,
		**keyword_arguments: Any,
	) -> tuple[Any, ...]:
		return (
			first,
			second,
			arguments,
			enabled,
			keyword_arguments,
		)

	namespace = Namespace(
		func=_function,
		first=POSITIONAL_ONLY_ARGUMENT,
		second=POSITIONAL_OR_KEYWORD_ARGUMENT,
		arguments=VARIABLE_POSITIONAL_ARGUMENTS,
		enabled=KEYWORD_ONLY_ARGUMENT,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_positional_arguments_are_preserved():
			assert actual[0] == POSITIONAL_ONLY_ARGUMENT
			assert actual[1] is POSITIONAL_OR_KEYWORD_ARGUMENT

		def Then_the_variable_positional_arguments_are_preserved():
			assert actual[2] == VARIABLE_POSITIONAL_ARGUMENTS

		def Then_the_keyword_only_argument_is_preserved():
			assert actual[3] is KEYWORD_ONLY_ARGUMENT

		def Then_the_remaining_arguments_are_preserved():
			assert actual[4] == REMAINING_ARGUMENTS


# ---------------------------------------------------------------------------
# Argument identity
# ---------------------------------------------------------------------------

def Given_an_argument_value_that_must_not_be_copied():

	ARGUMENT = object()

	def _function(value: object) -> object:
		return value

	namespace = Namespace(
		func=_function,
		value=ARGUMENT,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_same_argument_object_is_passed():
			assert actual is ARGUMENT


def Given_a_variable_positional_argument_that_must_not_be_copied():

	ARGUMENT = object()
	ARGUMENTS = (ARGUMENT,)

	def _function(*arguments: Any) -> tuple[Any, ...]:
		return arguments

	namespace = Namespace(
		func=_function,
		arguments=ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_same_argument_object_is_passed():
			assert actual[0] is ARGUMENT


def Given_a_remaining_argument_that_must_not_be_copied():

	ARGUMENT = object()
	REMAINING_ARGUMENTS = {
		"value": ARGUMENT,
	}

	def _function(**arguments: Any) -> dict[str, Any]:
		return arguments

	namespace = Namespace(
		func=_function,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_same_argument_object_is_passed():
			assert actual["value"] is ARGUMENT


# ---------------------------------------------------------------------------
# Complete composition
# ---------------------------------------------------------------------------

def Given_variable_positional_and_keyword_arguments():

	POSITIONAL_ARGUMENTS = ("Alice", 42)
	REMAINING_ARGUMENTS = {
		"enabled": True,
		"mode": "strict",
	}

	def _function(
		*arguments: Any,
		**keyword_arguments: Any,
	) -> tuple[tuple[Any, ...], dict[str, Any]]:
		return arguments, keyword_arguments

	namespace = Namespace(
		func=_function,
		arguments=POSITIONAL_ARGUMENTS,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_positional_arguments_are_expanded():
			assert actual[0] == POSITIONAL_ARGUMENTS

		def Then_the_remaining_arguments_are_passed_as_keywords():
			assert actual[1] == REMAINING_ARGUMENTS


def Given_arguments_for_all_parameter_kinds():

	POSITIONAL_ONLY_ARGUMENT = "Alice"
	POSITIONAL_OR_KEYWORD_ARGUMENT = 42
	VARIABLE_POSITIONAL_ARGUMENTS = ("one", "two")
	KEYWORD_ONLY_ARGUMENT = True
	REMAINING_ARGUMENTS = {
		"extra": "value",
	}

	def _function(
		name: str,
		age: int,
		/,
		*arguments: str,
		enabled: bool,
		**keyword_arguments: Any,
	) -> tuple[Any, ...]:
		return (
			name,
			age,
			arguments,
			enabled,
			keyword_arguments,
		)

	namespace = Namespace(
		func=_function,
		name=POSITIONAL_ONLY_ARGUMENT,
		age=POSITIONAL_OR_KEYWORD_ARGUMENT,
		arguments=VARIABLE_POSITIONAL_ARGUMENTS,
		enabled=KEYWORD_ONLY_ARGUMENT,
		**REMAINING_ARGUMENTS,
	)

	def When_the_function_is_dispatched():

		actual = dispatch(namespace)

		def Then_the_positional_arguments_are_passed():
			assert actual[0:2] == (
				POSITIONAL_ONLY_ARGUMENT,
				POSITIONAL_OR_KEYWORD_ARGUMENT,
			)

		def Then_the_variable_positional_arguments_are_expanded():
			assert actual[2] == VARIABLE_POSITIONAL_ARGUMENTS

		def Then_the_keyword_only_argument_is_passed():
			assert actual[3] is KEYWORD_ONLY_ARGUMENT

		def Then_the_remaining_arguments_are_passed():
			assert actual[4] == REMAINING_ARGUMENTS
