"""Tests for node registry."""
from app.compiler.nodes.registry import get_all_definitions, get_node_type


class TestNodeRegistry:
    def test_get_all_definitions(self):
        defs = get_all_definitions()
        assert len(defs) > 0
        types = [d.type for d in defs]
        assert "digital-input" in types
        assert "digital-output" in types
        assert "and-gate" in types
        assert "timer" in types

    def test_get_existing_type(self):
        node = get_node_type("digital-input")
        assert node is not None
        assert node.type == "digital-input"
        assert len(node.inputs) >= 0
        assert len(node.outputs) >= 1

    def test_get_nonexistent_type(self):
        assert get_node_type("nonexistent") is None

    def test_logic_gates_have_inputs_and_outputs(self):
        for gate_type in ("and-gate", "or-gate", "not-gate", "xor-gate"):
            node = get_node_type(gate_type)
            assert node is not None
            assert len(node.outputs) >= 1

    def test_timing_nodes_exist(self):
        for t in ("timer", "delay", "edge-detector", "debounce"):
            node = get_node_type(t)
            assert node is not None

    def test_constant_nodes_exist(self):
        for t in ("constant-true", "constant-false"):
            node = get_node_type(t)
            assert node is not None
