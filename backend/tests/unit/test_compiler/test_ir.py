"""Comprehensive tests for the IR builder and topological sort."""
from app.compiler.ir import IR, IREdge, IRNode, build_ir


def _make_graph(nodes, edges=None):
    return {"nodes": nodes, "edges": edges or []}


def _node(id, ntype, props=None):
    return {"id": id, "type": ntype, "data": {"properties": props or {}}}


class TestBuildIR:
    def test_empty_graph(self):
        ir = build_ir({"nodes": [], "edges": []})
        assert len(ir.nodes) == 0
        assert len(ir.edges) == 0
        assert len(ir.sorted_ids) == 0

    def test_single_node(self):
        ir = build_ir(_make_graph([_node("n1", "digital-input", {"gpio_pin": 4})]))
        assert len(ir.nodes) == 1
        assert ir.nodes[0].id == "n1"
        assert ir.nodes[0].type == "digital-input"
        assert ir.nodes[0].properties == {"gpio_pin": 4}
        assert ir.sorted_ids == ["n1"]

    def test_two_nodes_with_edge(self):
        ir = build_ir(_make_graph(
            [_node("a", "digital-input"), _node("b", "digital-output")],
            [{"source": "a", "target": "b", "sourceHandle": "out", "targetHandle": "in"}],
        ))
        assert len(ir.nodes) == 2
        assert len(ir.edges) == 1
        assert ir.sorted_ids == ["a", "b"]

    def test_topological_order_chain(self):
        ir = build_ir(_make_graph(
            [_node("c", "digital-output"), _node("a", "digital-input"), _node("b", "and-gate")],
            [{"source": "a", "target": "b"}, {"source": "b", "target": "c"}],
        ))
        # a must come before b, b before c
        order = ir.sorted_ids
        assert order.index("a") < order.index("b")
        assert order.index("b") < order.index("c")

    def test_ir_edge_handles_defaults(self):
        ir = build_ir(_make_graph(
            [_node("a", "digital-input"), _node("b", "digital-output")],
            [{"source": "a", "target": "b"}],
        ))
        assert ir.edges[0].source_handle == ""
        assert ir.edges[0].target_handle == ""


class TestIRDataclasses:
    def test_ir_node_defaults(self):
        node = IRNode(id="x", type="timer")
        assert node.properties == {}
        assert node.resolved_type == ""

    def test_ir_edge(self):
        edge = IREdge(source="a", source_handle="out", target="b", target_handle="in")
        assert edge.source == "a"
        assert edge.target == "b"

    def test_ir_container(self):
        ir = IR(nodes=[], edges=[], sorted_ids=[])
        assert len(ir.nodes) == 0
