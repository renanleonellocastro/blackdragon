"""Comprehensive tests for the IR optimizer."""
from app.compiler.ir import IR, IREdge, IRNode
from app.compiler.optimizer import optimize


def _ir(nodes, edges, sorted_ids=None):
    if sorted_ids is None:
        sorted_ids = [n.id for n in nodes]
    return IR(nodes=nodes, edges=edges, sorted_ids=sorted_ids)


class TestDeadNodeElimination:
    def test_removes_isolated_non_output_node(self):
        ir = _ir(
            [IRNode(id="dead", type="timer")],
            [],
        )
        result = optimize(ir)
        assert len(result.nodes) == 0

    def test_keeps_output_node(self):
        ir = _ir(
            [IRNode(id="out", type="digital-output", properties={"gpio_pin": 5})],
            [],
        )
        result = optimize(ir)
        assert len(result.nodes) == 1

    def test_keeps_chain_to_output(self):
        ir = _ir(
            [IRNode(id="in", type="digital-input"),
             IRNode(id="out", type="digital-output")],
            [IREdge(source="in", source_handle="out", target="out", target_handle="in")],
        )
        result = optimize(ir)
        assert len(result.nodes) == 2

    def test_removes_dead_branch(self):
        ir = _ir(
            [IRNode(id="in", type="digital-input"),
             IRNode(id="dead", type="timer"),
             IRNode(id="out", type="digital-output")],
            [IREdge(source="in", source_handle="out", target="out", target_handle="in")],
        )
        result = optimize(ir)
        ids = {n.id for n in result.nodes}
        assert "dead" not in ids
        assert "in" in ids
        assert "out" in ids


class TestConstantFolding:
    def test_folds_constant_true(self):
        ir = _ir(
            [IRNode(id="c", type="constant-true"),
             IRNode(id="out", type="digital-output")],
            [IREdge(source="c", source_handle="out", target="out", target_handle="in")],
        )
        result = optimize(ir)
        const_node = next(n for n in result.nodes if n.id == "c")
        assert const_node.properties.get("_resolved_value") is True

    def test_folds_constant_false(self):
        ir = _ir(
            [IRNode(id="c", type="constant-false"),
             IRNode(id="out", type="digital-output")],
            [IREdge(source="c", source_handle="out", target="out", target_handle="in")],
        )
        result = optimize(ir)
        const_node = next(n for n in result.nodes if n.id == "c")
        assert const_node.properties.get("_resolved_value") is False
