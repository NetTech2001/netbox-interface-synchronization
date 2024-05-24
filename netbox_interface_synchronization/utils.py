import re
from typing import Iterable
from dataclasses import dataclass


def split(s):
    for x, y in re.findall(r'(\d*)(\D*)', s):
        yield '', int(x or '0')
        yield y, 0


def natural_keys(c):
    return tuple(split(c))


def human_sorted(iterable: Iterable):
    return sorted(iterable, key=natural_keys)


@dataclass(frozen=True)
class UnifiedInterface:
    """A unified way to represent the interface and interface template"""
    id: int
    name: str
    type: str
    type_display: str
    mgmt_only: bool = False
    is_template: bool = False

    def __eq__(self, other):
        # Ignore some fields when comparing; ignore interface name case and whitespaces
        return (self.name.lower().replace(' ', '') == other.name.lower().replace(' ', '')) and (self.type == other.type)

    def __hash__(self):
        # Ignore some fields when hashing; ignore interface name case and whitespaces
        return hash((self.name.lower().replace(' ', ''), self.type))
