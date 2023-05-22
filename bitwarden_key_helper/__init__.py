import subprocess
from getpass import getpass
from typing import List

from serde.json import from_json

from bitwarden_key_helper.bw_types import PasswordEntry


def remove_duplicate_sequences(byte_string, separator=b"\x1b[37D\x1b[37C\x1b[2K\x1b[G"):
    """
    Seperator here is a magic sequence of escape characters that the `bw` cli
    uses to redraw the password prompt after every character is typed.
    """
    sequences = byte_string.split(separator)

    seen = set()
    deduplicated_sequences = []

    for seq in sequences:
        if seq not in seen:
            seen.add(seq)
            deduplicated_sequences.append(seq)

    # we drop the first because the escape sequence in our case is slightly
    # different the first go round which produces two final values
    return separator.join(deduplicated_sequences[1:])


def search_bw_one(search: str) -> str:
    """
    Wrap the `bw` bitwarden CLI to run a search command interactively.

    Returns the raw password
    """  # noqa: E501
    command = ["bw", "get", "password", search]
    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    input_str = getpass("bitwarden master password:")
    output, errors = process.communicate(input_str.encode())
    # The process' output and errors are also in bytes, so we decode them.
    output = output.decode()
    # TODO: maybe do something smart conditionally on errors
    errors = remove_duplicate_sequences(errors).decode()
    return output


def search_bw(search: str) -> List[PasswordEntry]:
    """
    Wrap the `bw` bitwarden CLI to run a search command interactively.

    Returns a list of PasswordEntry objects
    """  # noqa: E501
    command = ["bw", "list", "items", "--search", search]
    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    input_str = getpass("bitwarden master password:")
    output, errors = process.communicate(input_str.encode())

    # The process' output and errors are also in bytes, so we decode them.
    output = output.decode()
    errors = remove_duplicate_sequences(errors).decode()

    return from_json(List[PasswordEntry], output)
