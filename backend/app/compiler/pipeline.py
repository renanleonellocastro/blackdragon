"""Compiler pipeline orchestrator — validate → IR → optimize → generate."""
from dataclasses import dataclass
from typing import Any

from app.compiler.generators.esphome import ESPHomeGenerator
from app.compiler.generators.homeassistant import HomeAssistantGenerator
from app.compiler.ir import build_ir
from app.compiler.optimizer import optimize
from app.compiler.validator import ValidationResult, validate_graph

_GENERATORS = {
    "esphome": ESPHomeGenerator,
    "homeassistant": HomeAssistantGenerator,
}


@dataclass
class CompileResult:
    success: bool
    validation: ValidationResult
    output: str | None = None
    target: str = "esphome"


def compile_graph(
    graph_data: dict[str, Any],
    context: dict | None = None,
    target: str = "esphome",
) -> CompileResult:
    context = context or {}

    # Step 1: Validate
    validation = validate_graph(graph_data)
    if not validation.valid:
        return CompileResult(success=False, validation=validation)

    # Step 2: Build IR
    ir = build_ir(graph_data)

    # Step 3: Optimize
    ir = optimize(ir)

    # Step 4: Generate
    gen_cls = _GENERATORS.get(target, ESPHomeGenerator)
    generator = gen_cls()
    output = generator.generate(ir, context)

    return CompileResult(
        success=True,
        validation=validation,
        output=output,
        target=target,
    )


def validate_only(graph_data: dict[str, Any]) -> ValidationResult:
    return validate_graph(graph_data)
