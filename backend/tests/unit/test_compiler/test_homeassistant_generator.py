"""Tests for Home Assistant YAML generator."""
from app.compiler.generators.homeassistant import HomeAssistantGenerator
from app.compiler.ir import IR, IREdge, IRNode


def test_ha_generates_automation_from_input_to_output() -> None:
    ir = IR(
        nodes=[
            IRNode(id="input1", type="digital-input", properties={"gpio_pin": 4}),
            IRNode(id="output1", type="digital-output", properties={"gpio_pin": 5}),
        ],
        edges=[IREdge(source="input1", target="output1", source_port="out", target_port="in")],
        sorted_ids=["input1", "output1"],
    )
    gen = HomeAssistantGenerator()
    result = gen.generate(ir, {})
    assert "automation" in result
    assert "switch.toggle" in result


def test_ha_generates_timer_script() -> None:
    ir = IR(
        nodes=[
            IRNode(id="timer1", type="timer", properties={"duration_ms": 2000}),
        ],
        edges=[],
        sorted_ids=["timer1"],
    )
    gen = HomeAssistantGenerator()
    result = gen.generate(ir, {})
    assert "script" in result
    assert "2000" in result
