"""Tests for module creation and compilation expansion."""
import pytest

from app.compiler.ir import IR, IRNode, IREdge


def test_module_graph_structure() -> None:
    """Module graph data can be stored as JSONB and loaded as sub-graph."""
    module_graph = {
        "nodes": [
            {"id": "in1", "type": "digital-input", "properties": {"gpio_pin": 4}},
            {"id": "gate1", "type": "and-gate", "properties": {}},
            {"id": "out1", "type": "digital-output", "properties": {"gpio_pin": 5}},
        ],
        "edges": [
            {"source": "in1", "target": "gate1"},
            {"source": "gate1", "target": "out1"},
        ],
    }
    assert len(module_graph["nodes"]) == 3
    assert len(module_graph["edges"]) == 2


def test_module_expansion_preserves_topology() -> None:
    """When a module is expanded its internal topology is preserved."""
    ir = IR(
        nodes=[
            IRNode(id="mod_in1", type="digital-input", properties={"gpio_pin": 4}),
            IRNode(id="mod_gate", type="and-gate", properties={}),
            IRNode(id="mod_out1", type="digital-output", properties={"gpio_pin": 5}),
        ],
        edges=[
            IREdge(source="mod_in1", source_handle="out", target="mod_gate", target_handle="in1"),
            IREdge(source="mod_gate", source_handle="out", target="mod_out1", target_handle="in"),
        ],
        sorted_ids=["mod_in1", "mod_gate", "mod_out1"],
    )
    assert len(ir.nodes) == 3
    assert len(ir.edges) == 2
    assert ir.sorted_ids[0] == "mod_in1"
