# PTX DayZ Config Validator

A command-line tool from PTX Community for checking DayZ Central Economy `types.xml` files before deploying them to a server. It runs locally and leaves the input files intact.

## Quick start

Requires Python 3.10 or newer. The validator uses only the Python standard library. Download or clone this repository, open a terminal in the project directory, and run:

```sh
python validator.py path/to/types.xml
```

To check a base file and a custom override in one command:

```sh
python validator.py vanilla/types.xml custom/types.xml
```

Use `python validator.py --version` to display the installed version.

## What it checks

- XML syntax, the `<types>` root, and item names.
- Duplicate item names within each file.
- Integer fields, quantity ranges, and values such as `min` exceeding `nominal`.

The validator accepts UTF-8 XML with or without a byte order mark, supports partial economy overrides, and checks each file independently. Files are limited to 16 MiB. DOCTYPE declarations are rejected. Mission loading and item-class verification against installed mods are outside the scope of these checks.

| Exit code | Meaning |
| --- | --- |
| `0` | No validation errors. Warnings may still be present. |
| `1` | At least one file could not be read or contains validation errors. |
| `2` | Invalid command-line usage. |

Errors and warnings are written to standard error.

## Development and support

Run the test suite with `python -m unittest discover -s tests -v`. See the [GitHub Actions workflow](.github/workflows/test.yml) for the Python versions and static analysis checks used in CI.

Use [GitHub Issues](https://github.com/vladekptx/ptx-dayz-config-validator/issues) for bug reports and feature requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for pull requests, [SECURITY.md](SECURITY.md) for private vulnerability reporting, and [CHANGELOG.md](CHANGELOG.md) for version history.

## License

Maintained by PTX Community. Released under the [MIT License](LICENSE).
