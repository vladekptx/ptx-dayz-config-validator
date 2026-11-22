# PTX DayZ Config Validator

Check DayZ Central Economy `types.xml` files before uploading them to a server.
The validator reads local files and prints errors and warnings without modifying them.

## Usage

Requires Python 3.10 or newer. No third-party dependencies.

```text
python validator.py path/to/types.xml
python validator.py vanilla/types.xml custom/types.xml
```

The validator accepts UTF-8 XML, including files with a byte order mark. It
checks XML structure, duplicate names within each file, numeric fields and
quantity ranges. It supports partial entries used in overrides. It limits
each file to 16 MiB and rejects DOCTYPE declarations.

Errors are written to standard error and return exit code 1. Warnings also
appear on standard error and keep exit code 0. CLI usage errors return 2.
Files are checked independently. The validator does not load a mission or
verify that item classes exist in installed mods.

## Tests

```text
python -m unittest discover -s tests -v
```

Use GitHub Issues for bug reports and feature requests. See
[CONTRIBUTING.md](CONTRIBUTING.md) for pull requests and [SECURITY.md](SECURITY.md)
for vulnerability reports.

Independent community tool maintained by PTX Community. Licensed under the
[MIT License](LICENSE).
