"""Node type definitions for Digital I/O."""
from dataclasses import dataclass, field


@dataclass
class PortDef:
    id: str
    label: str
    type: str  # signal, boolean, number
    direction: str  # input, output


@dataclass
class PropertyDef:
    key: str
    label: str
    type: str  # string, number, boolean, select
    default: str | int | bool | None = None
    options: list[str] = field(default_factory=list)


@dataclass
class NodeTypeDef:
    type: str
    label: str
    category: str
    inputs: list[PortDef]
    outputs: list[PortDef]
    properties: list[PropertyDef]


DIGITAL_INPUT = NodeTypeDef(
    type="digital-input",
    label="Digital Input",
    category="Hardware",
    inputs=[],
    outputs=[PortDef("signal", "Signal", "signal", "output")],
    properties=[
        PropertyDef("gpio_pin", "GPIO Pin", "number", 0),
        PropertyDef("pull_mode", "Pull Mode", "select", "none", ["none", "up", "down"]),
        PropertyDef("inverted", "Inverted", "boolean", False),
    ],
)

DIGITAL_OUTPUT = NodeTypeDef(
    type="digital-output",
    label="Digital Output",
    category="Hardware",
    inputs=[PortDef("signal", "Signal", "signal", "input")],
    outputs=[],
    properties=[
        PropertyDef("gpio_pin", "GPIO Pin", "number", 0),
        PropertyDef("inverted", "Inverted", "boolean", False),
    ],
)
