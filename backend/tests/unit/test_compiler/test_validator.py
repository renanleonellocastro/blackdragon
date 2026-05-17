"""Comprehensive tests for the compiler validator."""
from app.compiler.validator import validate_graph


def _make_graph(nodes, edges=None):
    return {"nodes": nodes, "edges": edges or []}


def _node(id, ntype, props=None):
    return {"id": id, "type": ntype, "data": {"properties": props or {}}}


class TestValidateGraph:
    def test_empty_graph_is_valid(self):
        result = validate_graph({"nodes": [], "edges": []})
        assert result.valid is True
        assert len(result.errors) == 0

    def test_valid_simple_graph(self):
        graph = _make_graph(
            [_node("n1", "digital-input", {"gpio_pin": 4}),
             _node("n2", "digital-output", {"gpio_pin": 5})],
            [{"source": "n1", "target": "n2", "targetHandle": "in"}],
        )
        result = validate_graph(graph)
        assert result.valid is True

    def test_unknown_node_type(self):
        graph = _make_graph([_node("n1", "unknown-type")])
        result = validate_graph(graph)
        assert result.valid is False
        assert any("Unknown node type" in e.message for e in result.errors)

    def test_edge_source_not_found(self):
        graph = _make_graph(
            [_node("n1", "digital-input")],
            [{"source": "missing", "target": "n1"}],
        )
        result = validate_graph(graph)
        assert result.valid is False
        assert any("source" in e.message and "not found" in e.message for e in result.errors)

    def test_edge_target_not_found(self):
        graph = _make_graph(
            [_node("n1", "digital-input")],
            [{"source": "n1", "target": "missing"}],
        )
        result = validate_graph(graph)
        assert result.valid is False
        assert any("target" in e.message and "not found" in e.message for e in result.errors)

    def test_unconnected_input_warning(self):
        graph = _make_graph(
            [_node("n1", "and-gate")],
        )
        result = validate_graph(graph)
        # AND gate has 2 inputs, both unconnected → warnings
        assert len(result.warnings) >= 1

    def test_gpio_conflict(self):
        graph = _make_graph([
            _node("n1", "digital-input", {"gpio_pin": 4}),
            _node("n2", "digital-output", {"gpio_pin": 4}),
        ])
        result = validate_graph(graph)
        assert result.valid is False
        assert any("GPIO pin 4" in e.message for e in result.errors)

    def test_cycle_detection(self):
        graph = _make_graph(
            [_node("a", "digital-input"), _node("b", "digital-output")],
            [{"source": "a", "target": "b"}, {"source": "b", "target": "a"}],
        )
        result = validate_graph(graph)
        assert result.valid is False
        assert any("cycle" in e.message.lower() for e in result.errors)

    def test_no_gpio_conflict_different_pins(self):
        graph = _make_graph([
            _node("n1", "digital-input", {"gpio_pin": 4}),
            _node("n2", "digital-output", {"gpio_pin": 5}),
        ])
        result = validate_graph(graph)
        # No GPIO conflict errors
        gpio_errors = [e for e in result.errors if "GPIO" in e.message]
        assert len(gpio_errors) == 0
