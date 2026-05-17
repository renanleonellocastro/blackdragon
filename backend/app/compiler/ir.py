"""Intermediate Representation with topological sort."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class IRNode:
    id: str
    type: str
    properties: dict[str, Any] = field(default_factory=dict)
    resolved_type: str = ""


@dataclass
class IREdge:
    source: str
    source_handle: str
    target: str
    target_handle: str


@dataclass
class IR:
    nodes: list[IRNode]
    edges: list[IREdge]
    sorted_ids: list[str]


def build_ir(graph_data: dict[str, Any]) -> IR:
    nodes_raw = graph_data.get("nodes", [])
    edges_raw = graph_data.get("edges", [])

    ir_nodes = []
    for n in nodes_raw:
        ir_nodes.append(IRNode(
            id=n["id"],
            type=n.get("type", ""),
            properties=n.get("data", {}).get("properties", {}),
        ))

    ir_edges = []
    for e in edges_raw:
        ir_edges.append(IREdge(
            source=e["source"],
            source_handle=e.get("sourceHandle", ""),
            target=e["target"],
            target_handle=e.get("targetHandle", ""),
        ))

    sorted_ids = _topological_sort(ir_nodes, ir_edges)

    return IR(nodes=ir_nodes, edges=ir_edges, sorted_ids=sorted_ids)


def _topological_sort(nodes: list[IRNode], edges: list[IREdge]) -> list[str]:
    adj: dict[str, list[str]] = {n.id: [] for n in nodes}
    in_degree: dict[str, int] = {n.id: 0 for n in nodes}

    for edge in edges:
        if edge.source in adj and edge.target in in_degree:
            adj[edge.source].append(edge.target)
            in_degree[edge.target] += 1

    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    result: list[str] = []

    while queue:
        queue.sort()  # Deterministic ordering
        nid = queue.pop(0)
        result.append(nid)
        for neighbor in adj.get(nid, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result
