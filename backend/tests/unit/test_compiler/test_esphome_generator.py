"""Comprehensive tests for the ESPHome generator."""
import yaml

from app.compiler.generators.esphome import ESPHomeGenerator
from app.compiler.ir import IR, IREdge, IRNode


def _ir(nodes, edges, sorted_ids=None):
    if sorted_ids is None:
        sorted_ids = [n.id for n in nodes]
    return IR(nodes=nodes, edges=edges, sorted_ids=sorted_ids)


class TestESPHomeGenerator:
    def test_file_extension(self):
        gen = ESPHomeGenerator()
        assert gen.file_extension() == ".yaml"

    def test_minimal_config(self):
        ir = _ir([], [])
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        assert config["esphome"]["name"] == "blackdragon-device"
        assert config["esphome"]["platform"] == "ESP32"
        assert "ota" in config
        assert "api" in config

    def test_wifi_config(self):
        ir = _ir([], [])
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {"wifi_ssid": "MyNet", "wifi_password": "pw123"})
        config = yaml.safe_load(result)
        assert config["wifi"]["ssid"] == "MyNet"
        assert config["wifi"]["password"] == "pw123"

    def test_binary_sensor_from_digital_input(self):
        ir = _ir(
            [IRNode(id="in1", type="digital-input", properties={"gpio_pin": 4, "pull_mode": "up"})],
            [],
        )
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        sensors = config.get("binary_sensor", [])
        assert len(sensors) == 1
        assert sensors[0]["pin"]["number"] == 4
        assert sensors[0]["pin"]["mode"]["pullup"] is True

    def test_digital_output_generates_switch_and_output(self):
        ir = _ir(
            [IRNode(id="out1", type="digital-output", properties={"gpio_pin": 5})],
            [],
        )
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        assert len(config.get("output", [])) == 1
        assert len(config.get("switch", [])) == 1
        assert config["output"][0]["pin"]["number"] == 5

    def test_inverted_pin(self):
        ir = _ir(
            [IRNode(id="in1", type="digital-input", properties={"gpio_pin": 4, "inverted": True})],
            [],
        )
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        assert config["binary_sensor"][0]["pin"]["inverted"] is True

    def test_debounce_filter(self):
        ir = _ir(
            [IRNode(id="in1", type="digital-input", properties={"gpio_pin": 4}),
             IRNode(id="db1", type="debounce", properties={"delay_ms": 100})],
            [IREdge(source="in1", source_handle="out", target="db1", target_handle="in")],
        )
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        sensors = config.get("binary_sensor", [])
        assert len(sensors) == 1
        assert any("delayed_on_off" in f for f in sensors[0].get("filters", []))

    def test_custom_esphome_name(self):
        ir = _ir([], [])
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {"esphome_name": "my-device", "board_variant": "nodemcu-32s"})
        config = yaml.safe_load(result)
        assert config["esphome"]["name"] == "my-device"
        assert config["esphome"]["board"] == "nodemcu-32s"

    def test_pull_down_mode(self):
        ir = _ir(
            [IRNode(id="in1", type="digital-input", properties={"gpio_pin": 4, "pull_mode": "down"})],
            [],
        )
        gen = ESPHomeGenerator()
        result = gen.generate(ir, {})
        config = yaml.safe_load(result)
        assert config["binary_sensor"][0]["pin"]["mode"]["pulldown"] is True
