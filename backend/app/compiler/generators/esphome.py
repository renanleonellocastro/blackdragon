"""ESPHome YAML generator — maps IR nodes to ESPHome component config."""
import yaml

from app.compiler.generators.base import BaseGenerator
from app.compiler.ir import IR, IRNode


class ESPHomeGenerator(BaseGenerator):
    def file_extension(self) -> str:
        return ".yaml"

    def generate(self, ir: IR, context: dict) -> str:
        config: dict = {}

        # ESPHome core config
        config["esphome"] = {
            "name": context.get("esphome_name", "blackdragon-device"),
            "platform": context.get("platform", "ESP32"),
            "board": context.get("board_variant", "esp32dev"),
        }

        # WiFi
        if context.get("wifi_ssid"):
            config["wifi"] = {
                "ssid": context["wifi_ssid"],
                "password": context.get("wifi_password", ""),
            }

        # OTA
        config["ota"] = {"platform": "esphome"}
        if context.get("ota_password"):
            config["ota"]["password"] = context["ota_password"]

        # API
        config["api"] = {}
        if context.get("api_password"):
            config["api"]["password"] = context["api_password"]

        # Logger
        config["logger"] = {}

        # Process nodes
        node_map = {n.id: n for n in ir.nodes}
        binary_sensors: list[dict] = []
        switches: list[dict] = []
        outputs: list[dict] = []

        for node_id in ir.sorted_ids:
            node = node_map.get(node_id)
            if not node:
                continue

            if node.type == "digital-input":
                sensor = self._generate_binary_sensor(node, ir)
                binary_sensors.append(sensor)

            elif node.type == "digital-output":
                output, switch = self._generate_output(node, ir)
                outputs.append(output)
                switches.append(switch)

        if binary_sensors:
            config["binary_sensor"] = binary_sensors
        if outputs:
            config["output"] = outputs
        if switches:
            config["switch"] = switches

        return yaml.dump(config, default_flow_style=False, sort_keys=False)

    def _generate_binary_sensor(self, node: IRNode, ir: IR) -> dict:
        props = node.properties
        sensor: dict = {
            "platform": "gpio",
            "id": self._safe_id(node.id),
            "name": node.properties.get("label", f"Input {props.get('gpio_pin', 0)}"),
            "pin": {
                "number": int(props.get("gpio_pin", 0)),
                "mode": {"input": True},
            },
        }

        pull_mode = props.get("pull_mode", "none")
        if pull_mode == "up":
            sensor["pin"]["mode"]["pullup"] = True
        elif pull_mode == "down":
            sensor["pin"]["mode"]["pulldown"] = True

        if props.get("inverted"):
            sensor["pin"]["inverted"] = True

        # Add filters from downstream nodes
        filters = self._collect_filters(node.id, ir)
        if filters:
            sensor["filters"] = filters

        return sensor

    def _generate_output(self, node: IRNode, ir: IR) -> tuple[dict, dict]:
        props = node.properties
        gpio_pin = int(props.get("gpio_pin", 0))
        safe_id = self._safe_id(node.id)

        output = {
            "platform": "gpio",
            "id": f"{safe_id}_output",
            "pin": {
                "number": gpio_pin,
                "mode": {"output": True},
            },
        }

        if props.get("inverted"):
            output["pin"]["inverted"] = True

        switch = {
            "platform": "output",
            "id": safe_id,
            "name": f"Output {gpio_pin}",
            "output": f"{safe_id}_output",
        }

        return output, switch

    def _collect_filters(self, source_id: str, ir: IR) -> list[dict]:
        """Collect filter configurations from timing/debounce nodes downstream."""
        filters: list[dict] = []
        node_map = {n.id: n for n in ir.nodes}

        for edge in ir.edges:
            if edge.source != source_id:
                continue
            target = node_map.get(edge.target)
            if not target:
                continue
            if target.type == "debounce":
                delay_ms = int(target.properties.get("delay_ms", 50))
                filters.append({"delayed_on_off": f"{delay_ms}ms"})
            elif target.type == "delay":
                delay_ms = int(target.properties.get("delay_ms", 500))
                filters.append({"delayed_on": f"{delay_ms}ms"})

        return filters

    def _safe_id(self, node_id: str) -> str:
        return node_id.replace("-", "_").replace(" ", "_").lower()
