import argparse
import atexit
import shutil
import tempfile
from pathlib import Path as FilePath

import pytest

from darg.converters import existingDir, existingFile, path, fileSize, seconds


# ---------------------------------------------------------------------------
# Filesystem test infrastructure
# ---------------------------------------------------------------------------

TEMP_DIRECTORY = FilePath(tempfile.mkdtemp())


def cleanup():
	shutil.rmtree(TEMP_DIRECTORY, ignore_errors=True)


atexit.register(cleanup)


# ---------------------------------------------------------------------------
# Filesystem
# ---------------------------------------------------------------------------

def Given_an_existing_file():

	FILE = TEMP_DIRECTORY / "existing-file" / "example.txt"
	FILE.parent.mkdir()
	FILE.touch()

	def When_the_existing_file_is_converted():

		actual = existingFile(str(FILE))

		def Then_the_path_is_returned():
			assert actual == FILE


def Given_a_missing_file():

	FILE = TEMP_DIRECTORY / "missing-file" / "example.txt"

	def When_the_missing_file_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			existingFile(str(FILE))

		def Then_the_error_message_describes_the_missing_file():
			assert str(error.value) == f"not a file: {FILE}"


def Given_a_directory_instead_of_a_file():

	DIRECTORY = TEMP_DIRECTORY / "directory-instead-of-file"
	DIRECTORY.mkdir()

	def When_the_directory_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			existingFile(str(DIRECTORY))

		def Then_the_error_message_describes_the_invalid_file():
			assert str(error.value) == f"not a file: {DIRECTORY}"


def Given_an_existing_directory():

	DIRECTORY = TEMP_DIRECTORY / "existing-directory"
	DIRECTORY.mkdir()

	def When_the_existing_directory_is_converted():

		actual = existingDir(str(DIRECTORY))

		def Then_the_path_is_returned():
			assert actual == DIRECTORY


def Given_a_missing_directory():

	DIRECTORY = TEMP_DIRECTORY / "missing-directory"

	def When_the_missing_directory_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			existingDir(str(DIRECTORY))

		def Then_the_error_message_describes_the_missing_directory():
			assert str(error.value) == f"not a directory: {DIRECTORY}"


def Given_a_file_instead_of_a_directory():

	FILE = TEMP_DIRECTORY / "file-instead-of-directory.txt"
	FILE.touch()

	def When_the_file_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			existingDir(str(FILE))

		def Then_the_error_message_describes_the_invalid_directory():
			assert str(error.value) == f"not a directory: {FILE}"


def Given_a_missing_path():

	PATH = TEMP_DIRECTORY / "missing-path"

	def When_the_path_is_converted():

		actual = path(str(PATH))

		def Then_the_path_is_returned():
			assert actual == PATH


def Given_an_existing_path():

	PATH = TEMP_DIRECTORY / "existing-path.txt"
	PATH.touch()

	def When_the_path_is_converted():

		actual = path(str(PATH))

		def Then_the_path_is_returned():
			assert actual == PATH


# ---------------------------------------------------------------------------
# File sizes
# ---------------------------------------------------------------------------

def Given_a_file_size_without_a_unit():

	VALUE = "42"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_value_is_interpreted_as_bytes():
			assert actual == 42


def Given_a_file_size_with_fractional_bytes():

	VALUE = "1.5"

	def When_the_file_size_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			fileSize(VALUE)

		def Then_the_error_message_describes_the_invalid_value():
			assert str(error.value) == f"invalid file size: {VALUE}"


def Given_a_decimal_file_size_with_a_decimal_unit():

	VALUE = "1.5kb"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_value_is_multiplied_before_being_converted_to_integer():
			assert actual == 1500


def Given_a_file_size_with_a_decimal_unit():

	VALUE = "2mb"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_value_uses_a_power_of_1000():
			assert actual == 2_000_000


def Given_a_file_size_with_a_binary_unit():

	VALUE = "2mib"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_value_uses_a_power_of_1024():
			assert actual == 2 * 1024**2


def Given_a_file_size_with_a_prefix_without_b():

	VALUE = "2k"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_prefix_is_interpreted_as_a_decimal_unit():
			assert actual == 2_000


def Given_a_zero_file_size():

	VALUE = "0"

	def When_the_file_size_is_converted():

		actual = fileSize(VALUE)

		def Then_the_value_is_zero_bytes():
			assert actual == 0


def Given_a_negative_file_size():

	VALUE = "-1"

	def When_the_file_size_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			fileSize(VALUE)

		def Then_the_error_message_describes_the_invalid_value():
			assert str(error.value) == f"invalid file size: {VALUE}"


def Given_an_invalid_file_size():

	VALUE = "1x"

	def When_the_file_size_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			fileSize(VALUE)

		def Then_the_error_message_describes_the_invalid_value():
			assert str(error.value) == f"invalid file size: {VALUE}"


# ---------------------------------------------------------------------------
# Time units
# ---------------------------------------------------------------------------

def Given_a_duration_without_a_unit():

	VALUE = "42"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_interpreted_as_seconds():
			assert actual == 42


def Given_a_duration_in_milliseconds():

	VALUE = "500ms"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_converted_to_seconds():
			assert actual == 0.5


def Given_a_duration_in_seconds():

	VALUE = "2s"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_in_seconds():
			assert actual == 2


def Given_a_duration_in_minutes():

	VALUE = "2m"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_converted_to_seconds():
			assert actual == 120


def Given_a_duration_in_hours():

	VALUE = "2h"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_converted_to_seconds():
			assert actual == 7200


def Given_a_duration_in_days():

	VALUE = "2d"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_converted_to_seconds():
			assert actual == 172800


def Given_a_decimal_duration():

	VALUE = "1.5m"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_converted_to_seconds():
			assert actual == 90


def Given_a_zero_duration():

	VALUE = "0"

	def When_the_duration_is_converted():

		actual = seconds(VALUE)

		def Then_the_value_is_zero_seconds():
			assert actual == 0


def Given_a_negative_duration():

	VALUE = "-1s"

	def When_the_duration_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			seconds(VALUE)

		def Then_the_error_message_describes_the_invalid_value():
			assert str(error.value) == f"invalid time: {VALUE}"


def Given_an_invalid_duration():

	VALUE = "1x"

	def When_the_duration_is_converted():

		with pytest.raises(argparse.ArgumentTypeError) as error:
			seconds(VALUE)

		def Then_the_error_message_describes_the_invalid_value():
			assert str(error.value) == f"invalid time: {VALUE}"
