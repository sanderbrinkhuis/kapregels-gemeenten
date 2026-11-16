"""Kleine hulpfuncties voor namespace-agnostisch XML-parsen."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def iter_local(el: ET.Element, name: str):
    for e in el.iter():
        if local(e.tag) == name:
            yield e


def first_text(el: ET.Element, name: str) -> str:
    for e in iter_local(el, name):
        return norm("".join(e.itertext()))
    return ""


def all_texts(el: ET.Element, name: str) -> list[str]:
    return [norm("".join(e.itertext())) for e in iter_local(el, name)]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def text_of(el: ET.Element) -> str:
    return norm(" ".join(t for t in el.itertext()))
