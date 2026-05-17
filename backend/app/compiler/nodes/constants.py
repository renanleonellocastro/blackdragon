"""Node type definitions for Constant values."""
from app.compiler.nodes.digital_io import NodeTypeDef, PortDef

CONSTANT_TRUE = NodeTypeDef(
    type="constant-true",
    label="Constant TRUE",
    category="Constants",
    inputs=[],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)

CONSTANT_FALSE = NodeTypeDef(
    type="constant-false",
    label="Constant FALSE",
    category="Constants",
    inputs=[],
    outputs=[PortDef("out", "Out", "boolean", "output")],
    properties=[],
)
