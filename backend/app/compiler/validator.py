"""Semantic validator for visual graph data."""
from dataclasses import dataclass, field
from typing import Any

from app.compiler.nodes.registry import get_node_type


@dataclass
class ValidationError:
    node_id: str | None
    message: str
    severity: str = "error"  # error | warning


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)


def validate_graph(graph_data: dict[str, Any]) -> ValidationResult:
    errors: list[ValidationError] = []
    warnings: list[ValidationError] = []

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    node_map = {n["id"]: n for n in nodes}

    # 1. Validate node types exist
    for node in nodes:
        ntype = node.get("type", "")
        if not get_node_type(ntype):
            errors.append(ValidationError(node["id"], f"Unknown node type: {ntype}"))

    # 2. Validate edge connectivity
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src not in node_map:
            errors.append(ValidationError(None, f"Edge source '{src}' not found"))
        if tgt not in node_map:
            errors.append(ValidationError(None, f"Edge target '{tgt}' not found"))

    # 3. Check for unconnected required inputs
    connected_inputs: set[tuple[str, str]] = set()
    for edge in edges:
        connected_inputs.add((edge["target"], edge.get("targetHandle", "")))

    for node in nodes:
        node_def = get_node_type(node.get("type", ""))
        if not node_def:
            continue
        for inp in node_def.inputs:
            if (node["id"], inp.id) not in connected_inputs:
                warnings.append(ValidationError(node["id"], f"Input '{inp.label}' is not connected"))

    # 4. Check GPIO conflicts
    gpio_pins: dict[int, list[str]] = {}
    for node in nodes:
        props = node.get("data", {}).get("properties", {})
        pin = props.get("gpio_pin")
        if pin is not None:
            gpio_pins.setdefault(int(pin), []).append(node["id"])

    for pin, node_ids in gpio_pins.items():
        if len(node_ids) > 1:
            errors.append(ValidationError(
                node_ids[0],
                f"GPIO pin {pin} used by multiple nodes: {', '.join(node_ids)}",
            ))

    # 5. Cycle detection (Kahn's algorithm)
    adj: dict[str, list[str]] = {n["id"]: [] for n in nodes}
    in_degree: dict[str, int] = {n["id"]: 0 for n in nodes}
    for edge in edges:
        src, tgt = edge["source"], edge["target"]
        if src in adj and tgt in in_degree:
            adj[src].append(tgt)
            in_degree[tgt] += 1

    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    visited = 0
    while queue:
        nid = queue.pop(0)
        visited += 1
        for neighbor in adj.get(nid, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if visited < len(nodes):
        errors.append(ValidationError(None, "Graph contains a cycle"))

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )
