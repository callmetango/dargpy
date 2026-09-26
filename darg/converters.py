import argparse
import re
from pathlib import Path as FilePath

from darg import Type

_TIME_UNITS = {
	"ms": 0.001,
	"s": 1,
	"m": 60,
	"h": 3600,
	"d": 86400,
}


# Filesystem

def existingDir(value):
	path = FilePath(value)
	if not path.is_dir():
		raise argparse.ArgumentTypeError(f"not a directory: {value}")

	return path

ExistingDir = Type(existingDir)


def existingFile(value):
	path = FilePath(value)
	if not path.is_file():
		raise argparse.ArgumentTypeError(f"not a file: {value}")

	return path

ExistingFile = Type(existingFile)


def path(value):
	return FilePath(value)

Path = Type(path)


# Numbers

def nonNegative(value):
	value = int(value)
	if value < 0:
		raise argparse.ArgumentTypeError("must not be negative")

	return value

NonNegative = Type(nonNegative)


def positive(value):
	value = int(value)
	if value <= 0:
		raise argparse.ArgumentTypeError("must be positive")

	return value

Positive = Type(positive)


def nonNegativeFloat(value):
	value = float(value)
	if value < 0:
		raise argparse.ArgumentTypeError("must not be negative")

	return value

NonNegativeFloat = Type(nonNegativeFloat)


def positiveFloat(value):
	value = float(value)
	if value <= 0:
		raise argparse.ArgumentTypeError("must be positive")

	return value

PositiveFloat = Type(positiveFloat)


# Units

def fileSize(value):
	if not (match := re.fullmatch(r"(\d+(?:\.\d+)?)([kmgtp](?:i?b)?|b)?",
		value.strip().lower())):
		raise argparse.ArgumentTypeError(f"invalid file size: {value}")
	value, unit = match.groups()
	power = "kmgtp".find(unit[0]) + 1 if unit else 0
	base = 1024 if unit and "i" in unit else 1000
	size = float(value) * base**power
	if not size.is_integer():
		raise argparse.ArgumentTypeError(f"invalid file size: {value}")
	return int(size)

FileSize = Type(fileSize)


def seconds(value):
	if not (match := re.fullmatch(r"(\d+(?:\.\d+)?)(ms|[smhd])?",
		value.strip().lower())):
		raise argparse.ArgumentTypeError(f"invalid time: {value}")
	value, unit = match.groups()
	return float(value) * _TIME_UNITS.get(unit, 1)

Seconds = Type(seconds)


def milliseconds(value):
	return int(seconds(value) * 1000)

Milliseconds = Type(milliseconds)

