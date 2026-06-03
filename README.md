# Project 3: Enterprise Random Password Generator

This project generates secure passwords using Python's standard libraries.

## Features

- Secure randomness via `secrets` (not `random`).
- Configurable length and character groups.
- Optional enforcement of at least one character from each selected group.
- Entropy estimate to validate strength.
- Batch generation for multiple passwords.
- Optional ambiguous character exclusion (O, 0, l, 1).
- Save generated passwords to a file.

## Run

```bash
python password_generator.py
```

## Notes

- Length is validated between 8 and 64 by default.
- Symbols are drawn from `string.punctuation`.
