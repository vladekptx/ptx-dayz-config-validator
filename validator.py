"""Read-only validation for DayZ Central Economy types.xml files."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_FILE_BYTES = 16 * 1024 * 1024
FIELDS = ("nominal", "lifetime", "restock", "min", "quantmin", "quantmax", "cost")
INTEGER = re.compile(r"[+-]?[0-9]{1,20}")


def validate(path):
    """Return (errors, warnings) for one types.xml file."""
    try:
        with path.open("rb") as source:
            data = source.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            return ["File exceeds the 16 MiB size limit."], []
        text = data.decode("utf-8-sig")
        if re.search(r"<!DOCTYPE\b", text, re.IGNORECASE):
            return ["DOCTYPE declarations are unsupported."], []
        root = ET.fromstring(text)
    except (OSError, UnicodeError, ET.ParseError) as exc:
        return [str(exc)], []

    if root.tag != "types":
        return ["Expected a <types> root element."], []

    errors, warnings, seen = [], [], set()
    for index, item in enumerate(root, 1):
        if item.tag != "type":
            errors.append(f"Entry {index}: expected <type>, found <{item.tag}>.")
            continue
        name = item.get("name", "").strip()
        label = f"Entry {index}" + (f" ({name})" if name else "")
        if not name:
            errors.append(f"{label}: missing type name.")
        elif name in seen:
            errors.append(f"{label}: duplicate type name.")
        else:
            seen.add(name)

        values = {}
        for field in FIELDS:
            elements = item.findall(field)
            if not elements:
                continue  # Economy overrides can omit values.
            value = (elements[0].text or "").strip()
            if len(elements) != 1:
                errors.append(f"{label}: repeated <{field}>.")
            elif len(elements[0]) or not INTEGER.fullmatch(value):
                errors.append(f"{label}: <{field}> must contain an integer.")
            else:
                values[field] = int(value)

        for field, value in values.items():
            if field.startswith("quant"):
                if value != -1 and not 0 <= value <= 100:
                    errors.append(f"{label}: <{field}> must be -1 or 0–100.")
            elif value < 0:
                errors.append(f"{label}: <{field}> must be non-negative.")

        if {"min", "nominal"} <= values.keys() and 0 <= values["nominal"] < values["min"]:
            warnings.append(f"{label}: min exceeds nominal.")
        if {"quantmin", "quantmax"} <= values.keys() and 0 <= values["quantmax"] < values["quantmin"]:
            errors.append(f"{label}: quantmin exceeds quantmax.")

    if not len(root):
        warnings.append("No type entries were found.")
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=Path, nargs="+", help="DayZ types.xml files")
    args = parser.parse_args(argv)
    failed = False
    for path in args.files:
        errors, warnings = validate(path)
        for level, messages in (("ERROR", errors), ("WARNING", warnings)):
            for message in messages:
                print(f"{path}: {level}: {message}", file=sys.stderr)
        failed |= bool(errors)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
