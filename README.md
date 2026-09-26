# dargpy

> Bring light to `argparse`.

dargpy is a small Python domain-specific language (DSL) for defining command-line interfaces with [`argparse`](https://docs.python.org/3/library/argparse.html). It provides a lightweight, declarative interface while keeping `argparse` at its core.

## Installation

```console
python -m pip install dargpy
```

## Example

```python
from darg import Cli, OneOrMore, argument, command, dispatch, flag, option
from darg.converters import ExistingFile, NonNegative


def upload(tag, files, retries, verbose):
	print(tag, files)


cli = Cli(name="ghpy", about="GitHub release asset tool")

with cli:
	with command("release", about="Manage releases"):
		with command("upload", func=upload,
				about="Upload release assets"):
			option("retries", NonNegative, default=3)
			flag("verbose", alias="v", about="Enable verbose output")
			argument("tag")
			argument("files", OneOrMore, ExistingFile)

args = cli.parse_args()

dispatch(args)
```

The selected command is represented by a single command path:

```python
args._command
# "release/upload"
```

The selected command callable is available as:

```python
args.func
```

`dispatch()` maps the parsed values to the callable's Python signature. An optional instance can be supplied when the selected callable is an unbound method.

## Qualifiers

Qualifiers modify the `argparse` configuration of a declaration:

```python
from darg import Choices, Type

option("format", Choices("json", "yaml"))
argument("port", Type(int))
```

The built-in qualifiers include `Choices`, `Value`, `AppendValue`, `Count`, `OneOrMore`, and `Optional`.

## Converters

The `darg.converters` module provides common converters for turning command-line input into meaningful Python values, such as paths, sizes, and time units.

```python
from darg.converters import ExistingFile, FileSize, Seconds

argument("input", ExistingFile)
option("timeout", Seconds)
option("limit", FileSize)
```

Application developers can define additional converters for domain-specific values and expose them through `Type`:

```python
import argparse

from darg import Type


def repository(value):
	parts = value.split("/")
	if len(parts) != 2 or not all(parts):
		raise argparse.ArgumentTypeError("must be in OWNER/REPO format")

	return tuple(parts)


Repository = Type(repository)
```

## Dispatch

A command can be associated with a Python callable with `func`:

```python
with command("upload", func=Release.uploadAssets):
	argument("tag")
	argument("files", OneOrMore)
```

After parsing, the selected callable is available as `args.func`. The
selected command path is available as `args._command`.

`dispatch()` maps namespace values to the callable's signature. When invoking `dispatch()`, the namespace is sufficient for plain functions and bound methods:

```python
dispatch(args)
```

For an unbound method, pass the instance separately:

```python
dispatch(args, release)
```

A more elaborate example:

```python
args = cli.parse_args()

requests = RequestFactory(...)
releases = Releases(token, requests)
release = releases.getRelease(owner, repo, args.tag)

dispatch(args, release)
```

## Precedence

The declaration parameters `about`, `hint`, `default`, and `dest` take precedence over qualifier configuration and other keyword arguments. When multiple qualifiers configure the same `argparse` setting, the last qualifier wins.

## Why dargpy?

`argparse` is already a good command-line parser. dargpy makes structured CLI definitions concise and keeps the parser underneath rather than amassing machinery on top of it.

The structure remains visible in Python:

```python
with command("release"):
	with command("upload"):
		...
```

The goal is deliberately modest:

- Keep `argparse`.
- Keep the resulting `argparse.Namespace`.
- Use Python itself as the DSL.
- Let Python callables define the application boundary.
- Dispatch parsed values according to normal Python calling conventions.
- Add as little machinery as possible.

## Development

dargpy aims to be simple and clean, following [KISS and DRY](https://www.boldare.com/blog/kiss-yagni-dry-principles/). We care about separating concerns into their own modules, validating configuration at the boundary, and avoiding unnecessary machinery. PEP 8 not so much.

Install the development dependencies:

```console
python -m pip install -e ".[test]"
```

dargpy's tests use a Gherkin-style Given/When/Then structure with pytest. They are executable specifications, with fixtures used selectively for reusable context.

Run the tests with:

```console
python -m pytest
```

## Similar projects

[Climax](https://github.com/miguelgrinberg/climax) is a related lightweight project for building command-line interfaces around Python callables. It uses a decorator-based approach to define commands and their arguments.

## Status

dargpy is small and evolving. The API is not yet considered stable.

## License

GNU Lesser General Public License v3.0 only (LGPL-3.0-only).
