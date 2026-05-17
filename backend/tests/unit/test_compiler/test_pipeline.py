"""Tests for the full compiler pipeline."""
from app.compiler.pipeline import compile_graph, validate_only


def _node(id, ntype, props=None):
    return {"id": id, "type": ntype, "data": {"properties": props or {}}}


class TestCompilePipeline:
    def test_compile_valid_graph(self):
        graph = {
            "nodes": [
                _node("in1", "digital-input", {"gpio_pin": 4}),
                _node("out1", "digital-output", {"gpio_pin": 5}),
            ],
            "edges": [{"source": "in1", "target": "out1", "sourceHandle": "out", "targetHandle": "in"}],
        }
        result = compile_graph(graph)
        assert result.success is True
        assert result.output is not None
        assert "binary_sensor" in result.output
        assert result.target == "esphome"

    def test_compile_invalid_graph(self):
        graph = {"nodes": [_node("n1", "unknown-type")], "edges": []}
        result = compile_graph(graph)
        assert result.success is False
        assert result.output is None

    def test_compile_with_context(self):
        graph = {
            "nodes": [_node("in1", "digital-input", {"gpio_pin": 4})],
            "edges": [],
        }
        result = compile_graph(graph, context={"esphome_name": "test-device"})
        assert result.success is True
        assert "test-device" in result.output

    def test_compile_homeassistant_target(self):
        graph = {
            "nodes": [
                _node("in1", "digital-input", {"gpio_pin": 4}),
                _node("out1", "digital-output", {"gpio_pin": 5}),
            ],
            "edges": [{"source": "in1", "target": "out1"}],
        }
        result = compile_graph(graph, target="homeassistant")
        assert result.success is True
        assert result.target == "homeassistant"
        assert "automation" in result.output

    def test_validate_only(self):
        graph = {
            "nodes": [_node("in1", "digital-input", {"gpio_pin": 4})],
            "edges": [],
        }
        result = validate_only(graph)
        assert result.valid is True

    def test_validate_only_invalid(self):
        graph = {"nodes": [_node("n1", "fake-type")], "edges": []}
        result = validate_only(graph)
        assert result.valid is False

    def test_compile_empty_graph(self):
        graph = {"nodes": [], "edges": []}
        result = compile_graph(graph)
        assert result.success is True
        assert result.output is not None
