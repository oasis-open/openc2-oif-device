import os

from pathlib import Path
from typing import Any, Generator, List, Tuple
from pdoc import Context, Module, link_inheritance
from pdoc.html_helpers import _md

doc_path = Path("docs")
base_module = "sb_utils"
context = Context()
_md.registerExtensions([
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists"
], {})


def recursive_htmls(mod: Module) -> Generator[Tuple[List[str], str, bool], Any, None]:
    subs = mod.submodules()
    name = list(filter(None, mod.name.replace(base_module, "")[1:].split(".")))
    yield name, mod.html(), len(subs) > 0
    for sub in subs:
        yield from recursive_htmls(sub)


if __name__ == "__main__":
    print(f"Creating docs for `{base_module}`")
    module = Module(base_module, context=context)
    link_inheritance(context)
    doc_path.mkdir(exist_ok=True)

    rec_mods = recursive_htmls(module)
    for (name, html, subs) in rec_mods:
        print(f"write doc for {base_module}{'.' if name else ''}{'.'.join(name)}")
        if subs:
            mod_path = Path(os.path.join(doc_path.absolute(), *name, "index.html"))
        else:
            mod_path = Path(os.path.join(doc_path.absolute(), *name[:-1], f"{name[-1]}.html"))

        mod_path.parent.mkdir(exist_ok=True)
        with mod_path.open("w", encoding="utf-8") as f:
            f.write(html)
