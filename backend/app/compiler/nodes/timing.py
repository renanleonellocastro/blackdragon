"""Node type definitions for Timing components."""
from app.compiler.nodes.digital_io import NodeTypeDef, PortDef, PropertyDef

TIMER = NodeTypeDef(
    type="timer",
    label="Timer",
    category="Timing",
    inputs=[PortDef("trigger", "Trigger", "signal", "input")],
    outputs=[PortDef("out", "Out", "signal", "output")],
    properties=[PropertyDef("duration_ms", "Duration (ms)", "number", 1000)],
)

DELAY = NodeTypeDef(
    type="delay",
    label="Delay",
    category="Timing",
    inputs=[PortDef("in", "In", "signal", "input")],
    outputs=[PortDef("out", "Out", "signal", "output")],
    properties=[PropertyDef("delay_ms", "Delay (ms)", "number", 500)],
)

EDGE_DETECTOR = NodeTypeDef(
    type="edge-detector",
    label="Edge Detector",
    category="Timing",
    inputs=[PortDef("in", "In", "signal", "input")],
    outputs=[
        PortDef("rising", "Rising", "signal", "output"),
        PortDef("falling", "Falling", "signal", "output"),
    ],
    properties=[],
)

DEBOUNCE = NodeTypeDef(
    type="debounce",
    label="Debounce",
    category="Timing",
    inputs=[PortDef("in", "In", "signal", "input")],
    outputs=[PortDef("out", "Out", "signal", "output")],
    properties=[PropertyDef("delay_ms", "Delay (ms)", "number", 50)],
)
