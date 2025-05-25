#!/usr/bin/env python3
"""
name_flag_xor_codec.py – encode a name/flag pair to base-64 via XOR,
and recover the flag given the name and the base-64 text.

Author: (your name)
"""

from __future__ import annotations

import base64
import binascii
from typing import ByteString
import random
import string

# ────────────────────────────────────────────────────────────────────────────────
#  Low-level helper 0: None → flag
# ────────────────────────────────────────────────────────────────────────────────
def generate_random_six_character_ascii_flag_with_letters_and_digits() -> str:
    """
    Generate a random 6-character ASCII flag consisting of uppercase letters,
    lowercase letters, and digits (A-Z, a-z, 0-9).
    """
    allowed_characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    if len(allowed_characters) < 1:
        raise RuntimeError("Character set for flag generation is empty.")

    try:
        return ''.join(random.choices(allowed_characters, k=6))
    except Exception as err:
        raise RuntimeError("Failed to generate a random flag.") from err


# ────────────────────────────────────────────────────────────────────────────────
#  Low-level helper 1: ASCII → raw bytes
# ────────────────────────────────────────────────────────────────────────────────
def convert_ascii_string_to_bytes(ascii_text: str) -> bytes:
    """
    Convert an ASCII-only string into its raw bytes representation.
    """
    #if ascii_text is None:
    #    raise ValueError("Input text must not be None.")
    try:
        return ascii_text.encode("ascii")
    except UnicodeEncodeError as err:  # pragma: no cover
        raise ValueError("Input text contains non-ASCII characters.") from err


# ────────────────────────────────────────────────────────────────────────────────
#  Low-level helper 2: XOR (flag repeats to match the name length)
# ────────────────────────────────────────────────────────────────────────────────
def xor_name_bytes_with_flag_bytes_repeating_flag(
    name_bytes: ByteString, flag_bytes_exactly_six: ByteString
) -> bytes:
    """
    XOR arbitrary-length *name_bytes* with a 6-byte *flag_bytes_exactly_six*,
    repeating the flag as many times as necessary.
    """
    if not isinstance(name_bytes, (bytes, bytearray)):
        raise TypeError("name_bytes must be a bytes-like object.")
    if not isinstance(flag_bytes_exactly_six, (bytes, bytearray)):
        raise TypeError("flag_bytes_exactly_six must be a bytes-like object.")
    if len(flag_bytes_exactly_six) != 6:
        raise ValueError("flag_bytes_exactly_six must contain exactly six bytes.")
    #if len(name_bytes) == 0:
    #    raise ValueError("name_bytes must not be empty.")

    needed_repetitions = (len(name_bytes) + 5) // 6
    repeated_flag = (flag_bytes_exactly_six * needed_repetitions)[: len(name_bytes)]
    return bytes(nb ^ fb for nb, fb in zip(name_bytes, repeated_flag))


# ────────────────────────────────────────────────────────────────────────────────
#  Low-level helper 3: raw bytes → base-64 ASCII
# ────────────────────────────────────────────────────────────────────────────────
def convert_bytes_to_base64_ascii_string(raw_bytes: ByteString) -> str:
    """
    Convert raw bytes to a base-64 ASCII string (RFC-4648, no newlines).
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise TypeError("raw_bytes must be a bytes-like object.")
    return base64.b64encode(raw_bytes).decode("ascii")


# ────────────────────────────────────────────────────────────────────────────────
#  Public API – encoder
# ────────────────────────────────────────────────────────────────────────────────
def encode_ascii_name_and_ascii_flag_to_base64_ciphertext(
    ascii_name: str, ascii_flag_exactly_six: str
) -> str:
    """
    Encode *ascii_name* and *ascii_flag_exactly_six* (6 chars) into base-64
    by XORing them (flag repeats if the name is longer).
    """
    name_bytes = convert_ascii_string_to_bytes(ascii_name)
    flag_bytes = convert_ascii_string_to_bytes(ascii_flag_exactly_six)

    xor_bytes = xor_name_bytes_with_flag_bytes_repeating_flag(name_bytes, flag_bytes)
    return convert_bytes_to_base64_ascii_string(xor_bytes)


# ────────────────────────────────────────────────────────────────────────────────
#  Public API – decoder
# ────────────────────────────────────────────────────────────────────────────────
def decode_ascii_flag_from_ascii_name_and_base64_ciphertext(
    ascii_name: str, base64_ciphertext: str
) -> str:
    """
    Recover the original 6-character flag given *ascii_name* and the
    base-64 ciphertext returned by the encoder.
    """
    name_bytes = convert_ascii_string_to_bytes(ascii_name)

    try:
        cipher_bytes = base64.b64decode(base64_ciphertext, validate=True)
    except (binascii.Error, ValueError) as err:
        raise ValueError("Ciphertext is not valid base-64.") from err

    if len(cipher_bytes) != len(name_bytes):
        raise ValueError("Ciphertext length does not match the provided name length.")
    if len(name_bytes) < 6:
        raise ValueError(
            "Name must contain at least six characters to recover the full flag."
        )

    # XOR name with ciphertext → repeated flag
    repeated_flag_bytes = bytes(nb ^ cb for nb, cb in zip(name_bytes, cipher_bytes))
    flag_bytes = repeated_flag_bytes[:6]

    try:
        return flag_bytes.decode("ascii")
    except UnicodeDecodeError as err:  # pragma: no cover
        raise ValueError("Recovered flag contains non-ASCII bytes.") from err


# ────────────────────────────────────────────────────────────────────────────────
#  Tests
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import unittest

    class _NameFlagCodecTests(unittest.TestCase):
        def test_round_trip_medium_name(self) -> None:
            name = "AliceBB"  # 7 chars ≥ 6
            flag = "secret"
            b64 = encode_ascii_name_and_ascii_flag_to_base64_ciphertext(name, flag)
            self.assertEqual(
                decode_ascii_flag_from_ascii_name_and_base64_ciphertext(name, b64), flag
            )

        def test_round_trip_long_name(self) -> None:
            name = "Christopher"
            flag = "secret"
            b64 = encode_ascii_name_and_ascii_flag_to_base64_ciphertext(name, flag)
            self.assertEqual(
                decode_ascii_flag_from_ascii_name_and_base64_ciphertext(name, b64), flag
            )

        def test_invalid_flag_length(self) -> None:
            with self.assertRaises(ValueError):
                encode_ascii_name_and_ascii_flag_to_base64_ciphertext("BobBBB", "toolong")

        def test_non_ascii_input(self) -> None:
            with self.assertRaises(ValueError):
                encode_ascii_name_and_ascii_flag_to_base64_ciphertext("Áliceaa", "secret")

        def test_ciphertext_length_mismatch(self) -> None:
            with self.assertRaises(ValueError):
                decode_ascii_flag_from_ascii_name_and_base64_ciphertext("Bobbbb", "AAA=")


    unittest.main(verbosity=2)
