"""Cross-reference validation for the controlled documentation workflow."""

from __future__ import annotations

from .json_types import JsonObject, as_json_array, as_json_object
from . import reporter as reporter_module


def validate_workflow_references(
    workflow_data: JsonObject,
    reporter: reporter_module.Reporter,
) -> None:
    """Resolve workflow IDs after schema validation has established shape."""

    def indexed_ids(items: object, key: str, label: str) -> set[str]:
        values: list[str] = []
        for raw_item in as_json_array(items) or []:
            item = as_json_object(raw_item)
            value = item.get(key) if item is not None else None
            if isinstance(value, str):
                values.append(value)
        duplicates = sorted(
            {value for value in values if values.count(value) > 1}
        )
        for value in duplicates:
            reporter.error(f"duplicate workflow {label}: {value}")
        return set(values)

    state_ids = indexed_ids(workflow_data.get("states"), "state_id", "state")
    role_ids = indexed_ids(workflow_data.get("roles"), "role_id", "role")
    gate_ids = indexed_ids(workflow_data.get("gates"), "gate_id", "gate")
    contract_ids = indexed_ids(
        workflow_data.get("contracts"),
        "contract_id",
        "contract",
    )
    indexed_ids(
        workflow_data.get("transitions"),
        "transition_id",
        "transition",
    )

    metadata = as_json_object(workflow_data.get("workflow"))
    if metadata is not None:
        for field in ("initial_state", "successful_terminal_state"):
            value = metadata.get(field)
            if value not in state_ids:
                reporter.error(
                    f"workflow {field} references unknown state: {value}"
                )
        for role_field in (
            "owner_role",
            "approval_authority_role",
            "canonization_authority_role",
        ):
            value = metadata.get(role_field)
            if value not in role_ids:
                reporter.error(
                    f"workflow {role_field} references unknown role: {value}"
                )

    transitions = as_json_array(workflow_data.get("transitions")) or []
    for raw_transition in transitions:
        transition = as_json_object(raw_transition)
        if transition is None:
            continue
        transition_id = transition.get("transition_id", "<unknown>")
        for field in ("from_state", "to_state"):
            value = transition.get(field)
            if value not in state_ids:
                reporter.error(
                    f"{transition_id}: {field} references unknown state: {value}"
                )
        for role in as_json_array(transition.get("authorized_roles")) or []:
            if role not in role_ids:
                reporter.error(
                    f"{transition_id}: unknown authorized role: {role}"
                )
        for gate in as_json_array(transition.get("required_gates")) or []:
            if gate not in gate_ids:
                reporter.error(f"{transition_id}: unknown required gate: {gate}")
        for contract in as_json_array(
            transition.get("required_contracts")
        ) or []:
            if contract not in contract_ids:
                reporter.error(
                    f"{transition_id}: unknown required contract: {contract}"
                )

    initialization = as_json_object(workflow_data.get("initialization"))
    if initialization is not None:
        for role in as_json_array(
            initialization.get("authorized_roles")
        ) or []:
            if role not in role_ids:
                reporter.error(
                    f"initialization references unknown role: {role}"
                )
        for gate in as_json_array(
            initialization.get("required_gates")
        ) or []:
            if gate not in gate_ids:
                reporter.error(
                    f"initialization references unknown gate: {gate}"
                )
        for contract in as_json_array(
            initialization.get("required_contracts")
        ) or []:
            if contract not in contract_ids:
                reporter.error(
                    f"initialization references unknown contract: {contract}"
                )

    gates_by_id: dict[str, JsonObject] = {}
    for raw_gate in as_json_array(workflow_data.get("gates")) or []:
        gate = as_json_object(raw_gate)
        gate_id = gate.get("gate_id") if gate is not None else None
        if gate is not None and isinstance(gate_id, str):
            gates_by_id[gate_id] = gate
    for required_gate in ("G-ARCH", "G0", "G1"):
        gate = gates_by_id.get(required_gate)
        if not gate:
            reporter.error(f"workflow does not define {required_gate}")
            continue
        if gate.get("implementation_status") != "IMPLEMENTED":
            reporter.error(f"{required_gate} must be IMPLEMENTED")
        if gate.get("blocking") is not True:
            reporter.error(f"{required_gate} must be blocking")
        evaluator = as_json_object(gate.get("evaluator"))
        if evaluator is None or not evaluator.get("command"):
            reporter.error(f"{required_gate} must define an evaluator command")
