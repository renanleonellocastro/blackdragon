"""Node type definitions for Logic Gates."""
from app.compiler.nodes.digital_io import NodeTypeDef, PortDef

AND_GATE = NodeTypeDef(
    type="and-gate",
    label="AND Gate",
    category="Logic",
    inputs=[
        PortDef("a", "A", "boolean", "input"),
        PortDef("b", "B", "boolean", "input"),
    ],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)

OR_GATE = NodeTypeDef(
    type="or-gate",
    label="OR Gate",
    category="Logic",
    inputs=[
        PortDef("a", "A", "boolean", "input"),
        PortDef("b", "B", "boolean", "input"),
    ],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)

NOT_GATE = NodeTypeDef(
    type="not-gate",
    label="NOT Gate",
    category="Logic",
    inputs=[PortDef("in", "In", "boolean", "input")],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)

XOR_GATE = NodeTypeDef(
    type="xor-gate",
    label="XOR Gate",
    category="Logic",
    inputs=[
        PortDef("a", "A", "boolean", "input"),
        PortDef("b", "B", "boolean", "input"),
    ],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)
