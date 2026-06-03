"""Enterprise random password generator."""

from __future__ import annotations

import math
import secrets
import string


MIN_LENGTH = 8
MAX_LENGTH = 64
MAX_COUNT = 50
AMBIGUOUS_CHARS = set("O0l1I")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Please enter a number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("That is not a valid integer.")
            continue
        return value


def _read_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"{prompt} {suffix} ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please enter y or n.")


def _entropy_bits(length: int, pool_size: int) -> float:
    if length <= 0 or pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)


def _filter_ambiguous(pool: str, exclude: bool) -> str:
    if not exclude:
        return pool
    return "".join(ch for ch in pool if ch not in AMBIGUOUS_CHARS)


def generate_password(
    length: int,
    use_letters: bool,
    use_digits: bool,
    use_symbols: bool,
    require_each_selected: bool,
    exclude_ambiguous: bool,
) -> str:
    pools: list[str] = []
    required_chars: list[str] = []

    if use_letters:
        letters = _filter_ambiguous(string.ascii_letters, exclude_ambiguous)
        pools.append(letters)
        if require_each_selected:
            required_chars.append(secrets.choice(letters))
    if use_digits:
        digits = _filter_ambiguous(string.digits, exclude_ambiguous)
        pools.append(digits)
        if require_each_selected:
            required_chars.append(secrets.choice(digits))
    if use_symbols:
        pools.append(string.punctuation)
        if require_each_selected:
            required_chars.append(secrets.choice(string.punctuation))

    if not pools:
        raise ValueError("At least one character group must be enabled.")

    pool = "".join(pools)
    if length < len(required_chars):
        raise ValueError("Length too short for required character groups.")

    remaining = length - len(required_chars)
    chars = required_chars + [secrets.choice(pool) for _ in range(remaining)]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main() -> None:
    print("Enterprise Random Password Generator")
    print("------------------------------------")

    length = _read_int(f"Password length ({MIN_LENGTH}-{MAX_LENGTH}): ")
    if length < MIN_LENGTH or length > MAX_LENGTH:
        print(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
        return

    use_letters = _read_yes_no("Include letters?", default=True)
    use_digits = _read_yes_no("Include digits?", default=True)
    use_symbols = _read_yes_no("Include symbols?", default=True)
    require_each = _read_yes_no("Require at least one from each selected group?", default=True)
    exclude_ambiguous = _read_yes_no("Exclude ambiguous chars (O, 0, l, 1)?", default=False)
    count = _read_int(f"How many passwords? (1-{MAX_COUNT}): ")
    if count < 1 or count > MAX_COUNT:
        print(f"Count must be between 1 and {MAX_COUNT}.")
        return
    save_to_file = _read_yes_no("Save passwords to a file?", default=False)
    output_path = ""
    if save_to_file:
        output_path = input("Output file path (e.g., passwords.txt): ").strip()
        if not output_path:
            print("Output path cannot be empty.")
            return

    try:
        passwords = [
            generate_password(
                length=length,
                use_letters=use_letters,
                use_digits=use_digits,
                use_symbols=use_symbols,
                require_each_selected=require_each,
                exclude_ambiguous=exclude_ambiguous,
            )
            for _ in range(count)
        ]
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    pool_size = 0
    if use_letters:
        pool_size += len(_filter_ambiguous(string.ascii_letters, exclude_ambiguous))
    if use_digits:
        pool_size += len(_filter_ambiguous(string.digits, exclude_ambiguous))
    if use_symbols:
        pool_size += len(string.punctuation)

    entropy = _entropy_bits(length, pool_size)

    label = "Generated password" if count == 1 else f"Generated passwords ({count})"
    print(f"\n{label}:")
    for password in passwords:
        print(password)
    print(f"Entropy estimate: {entropy:.2f} bits")

    if save_to_file:
        try:
            with open(output_path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(passwords) + "\n")
            print(f"Saved to: {output_path}")
        except OSError as exc:
            print(f"Could not write file: {exc}")


if __name__ == "__main__":
    main()
