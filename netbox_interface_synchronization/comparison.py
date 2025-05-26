from dataclasses import dataclass
from django.conf import settings

config = settings.PLUGINS_CONFIG["netbox_interface_synchronization"]


@dataclass(frozen=True)
class ParentComparison:
    """Common fields of a device component"""

    id: int
    name: str
    label: str
    description: str

    def __eq__(self, other):
        # Ignore some fields when comparing; ignore component name case and whitespaces
        eq = (
            self.name.lower().replace(" ", "") == other.name.lower().replace(" ", "")
        ) and (self.label == other.label)

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        # Ignore some fields when hashing; ignore component name case and whitespaces
        return hash(self.name.lower().replace(" ", ""))

    def __str__(self):
        return f"Label: {self.label}\nDescription: {self.description}"


@dataclass(frozen=True)
class ParentTypedComparison(ParentComparison):
    """Common fields of a device typed component"""

    type: str
    type_display: str

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash((self.name.lower().replace(" ", ""), self.type))

    def __str__(self):
        return f"{super().__str__()}\nType: {self.type_display}"


@dataclass(frozen=True)
class InterfaceComparison(ParentTypedComparison):
    """A unified way to represent the interface and interface template"""

    mgmt_only: bool
    is_template: bool = False

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
            and (self.mgmt_only == other.mgmt_only)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash((self.name.lower().replace(" ", ""), self.type))

    def __str__(self):
        return f"{super().__str__()}\nManagement only: {self.mgmt_only}"


@dataclass(frozen=True)
class FrontPortComparison(ParentTypedComparison):
    """A unified way to represent the front port and front port template"""

    color: str
    # rear_port_id: int
    rear_port_position: int
    is_template: bool = False

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
            and (self.color == other.color)
            and (self.rear_port_position == other.rear_port_position)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash((self.name.lower().replace(" ", ""), self.type))

    def __str__(self):
        return f"{super().__str__()}\nColor: {self.color}\nPosition: {self.rear_port_position}"


@dataclass(frozen=True)
class RearPortComparison(ParentTypedComparison):
    """A unified way to represent the rear port and rear port template"""

    color: str
    positions: int
    is_template: bool = False

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
            and (self.color == other.color)
            and (self.positions == other.positions)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash((self.name.lower().replace(" ", ""), self.type))

    def __str__(self):
        return f"{super().__str__()}\nColor: {self.color}\nPositions: {self.positions}"


@dataclass(frozen=True, eq=False)
class ConsolePortComparison(ParentTypedComparison):
    """A unified way to represent the consoleport and consoleport template"""

    is_template: bool = False


@dataclass(frozen=True, eq=False)
class ConsoleServerPortComparison(ParentTypedComparison):
    """A unified way to represent the consoleserverport and consoleserverport template"""

    is_template: bool = False


@dataclass(frozen=True)
class PowerPortComparison(ParentTypedComparison):
    """A unified way to represent the power port and power port template"""

    maximum_draw: str
    allocated_draw: str
    is_template: bool = False

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
            and (self.maximum_draw == other.maximum_draw)
            and (self.allocated_draw == other.allocated_draw)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash((self.name.lower().replace(" ", ""), self.type))

    def __str__(self):
        return f"{super().__str__()}\nMaximum draw: {self.maximum_draw}\nAllocated draw: {self.allocated_draw}"


@dataclass(frozen=True)
class PowerOutletComparison(ParentTypedComparison):
    """A unified way to represent the power outlet and power outlet template"""

    power_port_name: str = ""
    feed_leg: str = ""
    is_template: bool = False

    def __eq__(self, other):
        eq = (
            (self.name.lower().replace(" ", "") == other.name.lower().replace(" ", ""))
            and (self.label == other.label)
            and (self.type == other.type)
            and (self.power_port_name == other.power_port_name)
            and (self.feed_leg == other.feed_leg)
        )

        if config["compare_description"]:
            eq = eq and (self.description == other.description)

        return eq

    def __hash__(self):
        return hash(
            (self.name.lower().replace(" ", ""), self.type, self.power_port_name)
        )

    def __str__(self):
        return f"{super().__str__()}\nPower port name: {self.power_port_name}\nFeed leg: {self.feed_leg}"


@dataclass(frozen=True, eq=False)
class DeviceBayComparison(ParentComparison):
    """A unified way to represent the device bay and device bay template"""

    is_template: bool = False