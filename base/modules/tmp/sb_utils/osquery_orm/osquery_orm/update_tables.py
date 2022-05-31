"""
Update OSQuery tables
"""
import json
import os
import re

from functools import partial
from pathlib import Path
from string import Template
from typing import List

IgnoreTables = ["example", ]
NameOverride = {
    "os": "OS"
}
OperatingSystems = {
    "DARWIN": "MacOS",
    "FreeBSD": "FreeBSD",
    "LINUX": "Linux",
    "POSIX": "Posix",
    "WINDOWS": "Windows"
}
TypeMap = {
    # "AutoField
    # "BigAutoField
    "UNSIGNED_BIGINT": "BigIntegerField",
    "INTEGER": "IntegerField",
    "BIGINT": "BigIntegerField",
    # "SmallIntegerField": "SmallIntegerField",
    # "IdentityField": "IdentityField",
    # "FloatField": "FloatField",
    "DOUBLE": "DoubleField",
    # "DecimalField": "DecimalField",
    "CharField": "CharField",
    # "FixedCharField": "FixedCharField",
    "TEXT": "TextField",
    # "BlobField": "BlobField",
    # "BitField": "BitField",
    # "BigBitField": "BigBitField",
    # "UUIDField": "UUIDField",
    # "BinaryUUIDField": "BinaryUUIDField",
    "DATETIME": "DateTimeField",
    # "DateField: "DateField",
    # "TimeField: "TimeField",
    # "TimestampField": "TimestampField",
    # "IPField": "IPField",
    # "BooleanField": "BooleanField",
    # "BareField": "BareField",
    # "ForeignKey": "ForeignKeyField"
}
AliasFields = ("False", "def", "if", "raise", "None", "del", "import", "return", "True", "elif", "in", "try", "and",
               "else", "is", "while", "as", "except", "lambda", "with", "assert", "finally", "nonlocal", "yield",
               "break", "for", "not", "class", "from", "or", "continue", "global", "pass")
Substitutions = {
    "alf": "ALF",
    "apt": "APT",
    "arp": "ARP",
    "cpu": "CPU",
    "deb": "DEB",
    "dns": "DNS",
    "ec2": "EC2",
    "elf": "ELF",
    "ie": "IE",
    "lxd": "LXD",
    "nfs": "NFS",
    "ntfs": "NTFS",
    "nvram": "NVRAM",
    "oem": "OEM",
    "os": "OS",
    "pci": "PCI",
    "rpm": "RPM",
    "tls": "TLS",
    "tpm": "TPM",
    "usb": "USB",
    "wmi": "WMI"
}


def getClassName(_name: str):
    fixed_name = []
    for c in _name.split("_"):
        fixed_name.append(NameOverride.get(c.lower(), c.capitalize()))
    return "".join(fixed_name)


def getOperatingSystemExtentions(_os: str, cls: str):
    os_name = OperatingSystems.get(_os, _os)
    return f"class {os_name}_{cls}({cls}):"


def escapeText(txt: str) -> str:
    txt = txt.replace("\"", "\\\"")
    txt = txt.replace("'", "\\'")
    # txt = re.sub(r"\\([uU])", "\\\\\1", txt)
    return txt


def schemaName(_name: str, select: bool = True):
    words = _name.split("_")
    words = list(map(str.capitalize, words))
    name = "-".join([Substitutions.get(w.lower(), w) for w in words])
    return f"osquery:{'Select' if select else 'Data'}-{name}"


# Table functions
def table_name(attrs: dict, _name: str, *args, **kwargs):
    attrs.update(
        class_name=getClassName(_name),
        table_name=_name,
        metadata=f"\n\tclass Meta:\n\t\ttable_name = \"{_name}\"".replace("\t", " " * 4)
    )


def description(attrs: dict, desc: str):
    attrs["description"] = escapeText(desc)


def schema(attrs: dict, fields: List[str]):
    fields = "\n".join(fields)
    fields = re.sub(r"^", "\t", fields, flags=re.MULTILINE).replace("\t", "    ")
    attrs.update(
        schema=fields
    )


def schema_column(attrs: dict, _name: str, _type: str, desc: str, **kwargs):
    _type = TypeMap.get(_type, _type)
    attrs.setdefault("field_imports", set()).add(_type)
    args = {
        "help_text": f'"{escapeText(desc)}"'
    }
    if _name in AliasFields:
        args["column_name"] = f'"{_name}"'
        _name = f"{_name}_"
    field = f"{_name} = {_type}({', '.join(f'{k}={v}' for k, v in args.items())})"
    if kwargs:
        field += f"  # {kwargs}"
    attrs["fields"][_name] = escapeText(desc)
    return field


def schema_foreign_key(attrs: dict, column: str, table: str, **kwargs):
    cls = getClassName(table)
    attrs.setdefault("field_imports", set()).add("ForeignKeyField")
    attrs.setdefault("local_imports", set()).add(f"from .{table} import {cls}")
    field = f"{name} = ForeignKeyField({cls}, backref='{column}')"
    if kwargs:
        field += f"  # {kwargs}"
    return field


def extended_schema(attrs: dict, _os: str, fields: List[str]):
    ext_schema = f"\n\n# OS specific properties for {_os}"
    ext_schema += f"\n{getOperatingSystemExtentions(_os, attrs['class_name'])}\n"
    columns = "\n".join(fields)
    ext_schema += re.sub(r"^", "\t", columns, flags=re.MULTILINE).replace("\t", "    ")
    ext_schema += f"\n{attrs['metadata']}"
    attrs.setdefault("extended_schema", "")
    attrs["extended_schema"] += ext_schema.replace("\t", " " * 4) + "\n"


def implementation(attrs: dict, imp: str, **kwargs):
    pass


def fuzz_paths(attrs: dict, *paths):
    pass


def attributes(attrs: dict, **attr):
    pass


def examples(attrs: dict, exp: List[str]):
    attrs["description"] += "\n\tExamples:\n" + re.sub(r"^", "\t\t", "\n".join(exp), flags=re.MULTILINE)
    attrs["description"] = attrs["description"].replace("\t", "    ")


table_funcs = {
    "table_name": table_name,
    "description": description,
    "schema": schema,
    "Column": schema_column,
    "ForeignKey": schema_foreign_key,
    "extended_schema": extended_schema,
    "implementation": implementation,
    "fuzz_paths": fuzz_paths,
    "attributes": attributes,
    "examples": examples
}


def doc2table(doc: str) -> dict:
    attrs = {
        "general_imports": set(),
        "field_imports": set(),
        "local_imports": set(),
        "extended_schema": "",
        "description": "",
        "fields": {}
    }
    env_funcs = {
        **{k: partial(v, attrs) for k, v in table_funcs.items()},
        **OperatingSystems,
        **TypeMap
    }
    eval_env = {
        "locals": env_funcs,
        "globals": env_funcs,
        "__name__": "NAME",
        "__file__": "FILE",
        "__builtins__": env_funcs
    }

    with open(doc, "r") as d:
        spec = d.read()
        try:
            cc = compile(spec, doc, "exec")
            eval(cc, eval_env)
            attrs["description"] = re.sub("\t", "    ", f'''"""\n\t{attrs["description"]}\n\t"""''' if attrs["description"] else "")
            attrs["general_imports"] = ("\n".join(attrs["general_imports"]) + "\n") if attrs["general_imports"] else ""
            attrs["field_imports"] = attrs["field_imports"] - {"int", "str"}
            attrs["field_imports"] = f"from peewee import {', '.join(sorted(attrs['field_imports']))}\n" if attrs["field_imports"] else ""
            attrs["local_imports"] = ("\n".join(attrs["local_imports"]) + "\n\n") if attrs["local_imports"] else "\n"
            return attrs
        except Exception as err:
            raise Exception(f"Table parsing error has occurred: {err}") from err


if __name__ == "__main__":
    schema_const_tables = []
    schema_validation_tables = {
        "select": {},
        "data": {}
    }

    with open("table_template.txt", "r", encoding="UTF-8") as t:
        template_str = Template(t.read())
    spec_dir = os.path.abspath("./specs")
    table_dir = os.path.abspath("./tables")
    for (dirpath, dirnames, filenames) in os.walk(spec_dir):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if name in IgnoreTables:
                continue
            if ext == ".table":
                spec_path = os.sep.join([dirpath, filename])
                table_path = os.path.join(dirpath, f"{name}.py")
                table_path = table_path.replace(spec_dir, table_dir)
                print(f"Updating table for {spec_path}")
                opts = doc2table(spec_path)
                # Create JSON consts
                d = dirpath.split("/")[-1]
                desc = re.sub(r"\n\s+Examples:\n(.|\n)*", "", opts.get("description")[3:-3].strip())
                name = opts.get("table_name")
                schema_const_tables.append({
                    "const": name,
                    "description": f"{d.upper()}: {desc}".replace("\\\\", "")
                })
                schema_validation_tables["select"][schemaName(name)] = {
                    "name": name,
                    "desc": f"{d.upper()}: {desc}".replace("\\\\", ""),
                    "fields": opts["fields"],
                }
                schema_validation_tables["data"][schemaName(name, False)] = {}
                # Write PeeWee model
                Path(os.path.dirname(table_path)).mkdir(parents=True, exist_ok=True)
                with open(table_path, "w", encoding="UTF-8") as f:
                    f.write(template_str.substitute(opts))

    schema_const_tables = sorted(schema_const_tables, key=lambda i: i["const"])

    schema_tables = {
        "osquery:Select": {
            "title": "OSQuery Select",
            "type": "object",
            "description": "Query options for an OSQuery table",
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": False,
            "properties": {
                "general": {
                    "$ref": "#/definitions/osquery:Select-General"
                },
                **{d["name"]: {"$ref": f"#/definitions/osquery:Select-{t}"} for t, d in schema_validation_tables["select"].items()}
            }
        },
        "osquery:Tables": {
            "title": "OSQuery Table name",
            "type": "string",
            "description": "An array of zero to * names used to query a table for its data",
            "anyOf": schema_const_tables
        }
    }
    table_fields = {}

    for table, data in schema_validation_tables["select"].items():
        if table.startswith("osquery:Select-"):
            n = table[15:].lower().replace("-", "_")
            table_fields[n] = list(data["fields"].keys())
        schema_tables[table] = {
            "title": f"OSQuery Table Validation: {data['name']}",
            "type": "object",
            "description": data["desc"],
            "properties": {
                "columns": {
                    "type": "array",
                    "unique": True,
                    "items": {
                        "type": "string",
                        "oneOf": [{
                            "const": n,
                            "description": d
                        } for n, d in data["fields"].items()]
                    }
                },
                "filters": {
                  "type": "array",
                  "items": {
                    "$ref": "#/definitions/osquery:Filters"
                  }
                }
            }
        }

    with open("schema_tables.json", "w", encoding="UTF-8") as f:
        json.dump(schema_tables, f, indent=2)

    with open("table_fields.json", "w", encoding="UTF-8") as f:
        d = dict(sorted(table_fields.items()))
        json.dump(d, f, indent=2)
