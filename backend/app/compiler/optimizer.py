"""IR Optimizer — dead-node elimination and constant folding."""
from app.compiler.ir import IR, IREdge, IRNode


def optimize(ir: IR) -> IR:
    ir = _eliminate_dead_nodes(ir)
    ir = _fold_constants(ir)
    return ir


def _eliminate_dead_nodes(ir: IR) -> IR:
    """Remove nodes that have no downstream connections and no side effects."""
    side_effect_types = {"digital-output"}

    # Build reverse adjacency: which nodes are downstream of each node
    has_downstream: set[str] = set()
    for edge in ir.edges:
        has_downstream.add(edge.source)

    # Nodes with side effects or downstream connections are alive
    alive = set()
    for node in ir.nodes:
        if node.type in side_effect_types or node.id in has_downstream:
            alive.add(node.id)

    # Walk backwards: if a node is alive, its inputs are alive too
    changed = True
    while changed:
        changed = False
        for edge in ir.edges:
            if edge.target in alive and edge.source not in alive:
                alive.add(edge.source)
                changed = True

    # Filter
    new_nodes = [n for n in ir.nodes if n.id in alive]
    new_edges = [e for e in ir.edges if e.source in alive and e.target in alive]
    new_sorted = [sid for sid in ir.sorted_ids if sid in alive]

    return IR(nodes=new_nodes, edges=new_edges, sorted_ids=new_sorted)


def _fold_constants(ir: IR) -> IR:
    """Fold constant nodes through logic gates where possible."""
    node_map = {n.id: n for n in ir.nodes}

    # Find constant outputs
    constant_values: dict[str, bool] = {}
    for node in ir.nodes:
        if node.type == "constant-true":
            constant_values[node.id] = True
        elif node.type == "constant-false":
            constant_values[node.id] = False

    # Simple constant folding through logic gates
    # For now, just mark constant values on edges for the generator
    # Full folding would require iterative evaluation
    for node in ir.nodes:
        if node.id in constant_values:
            node.properties["_resolved_value"] = constant_values[node.id]

    return ir
