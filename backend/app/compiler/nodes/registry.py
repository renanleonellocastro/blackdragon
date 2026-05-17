"""Node type registry — centralized lookup for all node types."""
from app.compiler.nodes.constants import CONSTANT_FALSE, CONSTANT_TRUE
from app.compiler.nodes.digital_io import DIGITAL_INPUT, DIGITAL_OUTPUT, NodeTypeDef
from app.compiler.nodes.logic_gates import AND_GATE, NOT_GATE, OR_GATE, XOR_GATE
from app.compiler.nodes.timing import DEBOUNCE, DELAY, EDGE_DETECTOR, TIMER

_ALL_NODES: list[NodeTypeDef] = [
    DIGITAL_INPUT,
    DIGITAL_OUTPUT,
    AND_GATE,
    OR_GATE,
    NOT_GATE,
    XOR_GATE,
    TIMER,
    DELAY,
    EDGE_DETECTOR,
    DEBOUNCE,
    CONSTANT_TRUE,
    CONSTANT_FALSE,
]

REGISTRY: dict[str, NodeTypeDef] = {n.type: n for n in _ALL_NODES}


def get_node_type(node_type: str) -> NodeTypeDef | None:
    return REGISTRY.get(node_type)


def get_all_definitions() -> list[NodeTypeDef]:
    return _ALL_NODES
