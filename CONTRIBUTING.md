# Contributing

Open a GitHub issue with the expected result, the actual result and a small
sanitized XML example you have permission to share. For a fix, fork the project
and open a pull request with a description of the change and test results.

Run `python -m unittest discover -s tests -v` before sending a pull request.
Add a regression test when changing validation rules. Use synthetic examples
and keep the tool read-only. See [SECURITY.md](SECURITY.md) for private reports.
