"""Home Assistant YAML generator — maps IR nodes to HA automations."""
import yaml

from app.compiler.generators.base import BaseGenerator
from app.compiler.ir import IR, IRNode


class HomeAssistantGenerator(BaseGenerator):
    def file_extension(self) -> str:
        return ".yaml"

    def generate(self, ir: IR, context: dict) -> str:
        config: dict = {
            "homeassistant": {},
            "automation": [],
            "script": [],
        }

        node_map = {n.id: n for n in ir.nodes}

        for node_id in ir.sorted_ids:
            node = node_map.get(node_id)
            if not node:
                continue

            if node.type == "digital-input":
                config["automation"].append(self._input_automation(node, ir, node_map))
            elif node.type == "timer":
                config["script"].append(self._timer_script(node))

        # Clean empty sections
        config = {k: v for k, v in config.items() if v}

        return yaml.dump(config, default_flow_style=False, sort_keys=False)

    def _input_automation(self, node: IRNode, ir: IR, node_map: dict[str, IRNode]) -> dict:
        entity_id = f"binary_sensor.{self._safe_id(node.id)}"
        actions: list[dict] = []

        # Find connected outputs
        for edge in ir.edges:
            if edge.source != node.id:
                continue
            target = node_map.get(edge.target)
            if target and target.type == "digital-output":
                actions.append({
                    "service": "switch.toggle",
                    "target": {"entity_id": f"switch.{self._safe_id(target.id)}"},
                })

        return {
            "alias": f"Automation for {node.id}",
            "trigger": [{
                "platform": "state",
                "entity_id": entity_id,
                "to": "on",
            }],
            "action": actions or [{"service": "logger.log", "data": {"message": "No action configured"}}],
        }

    def _timer_script(self, node: IRNode) -> dict:
        duration_ms = int(node.properties.get("duration_ms", 1000))
        return {
            "alias": f"Timer {node.id}",
            "sequence": [
                {"delay": {"milliseconds": duration_ms}},
            ],
        }

    def _safe_id(self, node_id: str) -> str:
        return node_id.replace("-", "_").replace(" ", "_").lower()
