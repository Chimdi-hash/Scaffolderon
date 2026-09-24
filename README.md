# SCAFFOLDERON

SCAFFOLDERON is a reusable GenLayer primitive for intelligent, semantic state transitions. It enables a contract owner to define a state machine, register natural-language conditions for state transitions, and seal the configuration. An authorized operator can then request transitions, which are evaluated by GenLayer's optimistic democracy model. Only transitions evaluated as `APPROVED` will update the canonical state.

## Why SCAFFOLDERON

While traditional smart contracts excel at deterministic logic, real-world workflows often depend on nuanced, human-readable conditions that are difficult to encode using strict boolean logic. SCAFFOLDERON bridges this gap by maintaining deterministic lifecycle and state progression while delegating the evaluation of transition conditions to GenLayer's semantic consensus (LLM-based evaluation).

## How It Works

```text
SETUP → ADD RULE → ACTIVATE → EXECUTE → CONSENSUS → STATE CHANGE
```

1.  **Create:** A sender creates a new Workflow and becomes its owner, specifying the initial state.
2.  **Add Rules:** The owner registers `source_state` → `target_state` transitions, assigning a natural language `criteria` (prompt) to each.
3.  **Activate:** The owner activates the workflow. The rules are frozen, and the workflow becomes live.
4.  **Execute:** The designated operator submits an execution request, providing `evidence` (context).
5.  **Consensus:** GenLayer evaluates if the provided `evidence` clearly satisfies the registered `criteria` for the transition.
6.  **Approved:** If the semantic evaluation returns `APPROVED`, the workflow moves to the target state and increments its version.
7.  **Rejected/Ambiguous:** If the result is `REJECTED` or `AMBIGUOUS`, the execution attempt is recorded, but the workflow's state remains unchanged.

## Lifecycle Phases

Every workflow goes through three distinct phases:

*   **`SETUP`**: The initial phase. The owner can add transition rules. Executions cannot be requested.
*   **`LIVE`**: The workflow has been activated. No new rules can be added, but the operator can request executions.
*   **`ARCHIVED`**: A terminal phase. The workflow is disabled, preventing further executions, though the history remains readable.

## Semantic Consensus

The contract utilizes the GenLayer non-deterministic execution model via:

```python
gl.vm.run_nondet(leader, validator)
```

Before triggering consensus, deterministic contract code validates authorization, workflow phase, replay protection, and captures a snapshot of the rule criteria, submitted evidence, and state labels. 

The leader node evaluates this snapshot and returns a JSON payload containing the `outcome`. The validator node performs the exact same semantic evaluation. GenLayer enforces the Equivalence Principle: the validator must independently reach the exact same normalized outcome as the leader.

Valid outcomes are strictly limited to `APPROVED`, `REJECTED`, and `AMBIGUOUS`.

## Contract Interface

The contract requires no constructor arguments.

### Writes

*   `create_workflow(title, operator, start_state) -> str`
*   `add_transition_rule(workflow_id, source_state, target_state, criteria) -> str`
*   `activate_workflow(workflow_id) -> None`
*   `execute_transition(workflow_id, rule_id, exec_key, evidence) -> str`
*   `disable_workflow(workflow_id) -> None`

### Views

*   `get_workflow(workflow_id) -> dict`
*   `get_workflow_phase(workflow_id) -> str`
*   `get_rule(rule_id) -> dict`
*   `get_execution(exec_id) -> dict`
*   `get_my_latest_workflow() -> str`

## State & Integrity

All records are stored using GenLayer's `TreeMap`. 
Each workflow tracks its `version`, which increments only upon an `APPROVED` transition.

Domain-separated SHA-256 commitments ensure strict cryptographic binding:
*   **Workflow Hash:** Binds the workflow's immutable identity and configuration.
*   **Rule Hash:** Binds the specific criteria and allowed states.
*   **Execution Hash:** Binds the exact workflow version, rule, and evidence submitted.

The contract does not rely on unbounded loops to traverse all records; latest-record pointers are provided for discovery conveniences, while cryptographic digests maintain historical canonical integrity.

## Trust Model

SCAFFOLDERON evaluates whether the *submitted evidence* satisfies the *registered criteria*. It does not actively fetch web pages, consult external oracles, or independently verify real-world facts unless explicitly provided in the `evidence` payload. 

The semantic evaluator treats all conditions and evidence as untrusted data. This design establishes a defensive boundary, ensuring that prompt injection attempts or malicious evidence are constrained by the rigid output format (`APPROVED`, `REJECTED`, `AMBIGUOUS`).

## Deployment

Designed for deployment on the GenLayer Studio Net network.

| Field | Value |
|---|---|
| Network | GenLayer Studio Net |
| SDK Dependency | `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6` |
| **Contract Address** | `0x09036215457e52E618899dFFF299c2F601f23774` |
| **Explorer** | [View on GenLayer Explorer](https://explorer-studio.genlayer.com/address/0x09036215457e52E618899dFFF299c2F601f23774) |

## Verification

The source code in `contracts/Scaffolderon.py` serves as the canonical behavioral specification.
- Uses exact GenLayer dependencies.
- Free of unbounded loops.
- Compliant with GenVM deterministic limitations outside of `gl.vm.run_nondet`.
