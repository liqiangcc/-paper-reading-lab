---
name: source-first-reading
description: Execute one bounded paper-reading-lab source-first ReadingSession action from GitHub durable state using reading-mcp canonical Source. Use for starting, continuing, “下一句/下一步”, fresh-conversation recovery, current-source fidelity review, or safe pause/blocker handling. Do not use for generic repository audits, unrelated summaries, or PR governance.
---

# Source-First Reading

## Role

Execute **one authorized, bounded ReadingSession action**.

This Skill is a procedure, not method truth. It must follow:

- root `AGENTS.md`;
- `docs/workflows/conversation-bootstrap.md`;
- canonical Source / Session / workflow docs;
- the target Issue's latest applicable durable state;
- the exact bound Explanation Profile, if any.

Do not redefine Paper identity, SourceUnit identity, no-lookahead, scope or Profile semantics here.

## Required tools

```text
github-mcp
→ Issue / repository live state and durable writes

reading-mcp
→ canonical paper Source, structure, SourceUnit, locator and source view
```

For a clean first-pass Session, do not use Web, downstream analysis, Issue prose or model memory to obtain future paper body text.

## Bootstrap

Before any new Source reveal:

1. Read `AGENTS.md`.
2. Read the target Issue live state and relevant comments.
3. Follow `docs/workflows/conversation-bootstrap.md`.
4. Recover the latest applicable checkpoint / handoff / blocker / next action.
5. Load only the canonical docs needed for this action:
   - `docs/integrations/reading-mcp.md`;
   - `docs/learning/source-first-sentence-reading.md`;
   - `docs/learning/reading-sessions.md`;
   - `docs/workflows/paper-reading-lifecycle.md`;
   - `docs/workflows/issue-driven-workflow.md`;
   - `docs/validation/invariants.md`.
6. If a Profile is bound, read the exact `profile_id + version + source` from durable state.

Do not ask the user to re-paste a locator or Profile that GitHub durable state already contains.

## Recover required state

Verify before execution:

```text
paper_id
revision_id
reading provider / document identity
Session id / mode / lookahead policy
planned_scope
current_scope_boundary
revealed_position
latest precise SourceUnitRef / TextLocator
bound Profile identity（if any）
immutable prediction reference（if any）
current next_action
```

Missing or conflicting critical state fails closed.

## Scope gate

Before every new canonical reveal:

```text
next unit inside current_scope_boundary?
├── yes → continue
└── no  → STOP before reveal
          → durable scope amendment required
```

Never reveal first and amend scope afterwards.

If the boundary depends on a named paper section, use structure-only canonical navigation or a pre-validated boundary artifact. Do not use future-body lexical search as no-lookahead preflight.

## Canonical reveal

For ordinary sentence-first reading, default to:

```text
get_text_units(
  requested_kind = sentence,
  direction = forward,
  coverage_policy = preserve_source,
  max_items = 1,
  anchor_locator = latest precise locator
)
```

Use the current allowed `section_id` / owner from durable scope.

Rules:

- preserve provider order and actual kind;
- one canonical unit may contain multiple surface sentences;
- do not invent a parallel sentence identity;
- do not batch-read future units to find something “more useful”;
- a structural / non-prose unit still counts as the returned canonical unit unless durable scope explicitly authorizes further filtering.

## Exact re-read

For the returned allowed unit call:

```text
read_document(document_id, target_locator)
```

Do not use fuzzy snippet search to recover a stale locator.

If exact re-read returns stale, identity mismatch, serialization failure or unsafe invocation failure:

```text
persist blocker / handoff when needed
→ do not fetch another unit
→ STOP
```

## Original-source fidelity

Use `get_source_view` only when the **current allowed Source** needs visual verification, such as a Figure, Table, Equation, Algorithm, multi-column layout or parser ambiguity.

Keep distinct:

```text
text Source Fact
original-page visual observation
AI visual interpretation
```

Seeing a whole page does not authorize use of unrevealed future text on that page.

## Explain the current unit

If a formal Profile is bound, follow that exact version.

If no formal Profile is bound, use only the minimal Source-first structure:

```text
canonical original
→ faithful translation / literal meaning
→ relation to revealed past
→ actual cognitive increment
→ current problem model update
→ Source Fact / Derived / Unknown
→ precise locator
→ STOP
```

Every explicit reasoning arrow must be traceable to revealed Source or remain explicitly Derived.

Do not inject modern implementation details or future sections into a historical paper explanation.

## Prediction action

When current mode requires Prediction evidence:

```text
persist immutable prediction
→ only then reveal actual next unit
→ append comparison
```

Never edit the original prediction after reveal.

A user “下一句” does not by itself authorize both a new prediction cycle and unlimited subsequent reading; follow the durable `next_action` and scope.

## Durable result

Do not copy every long explanation into the Primary Issue.

Write durable state at meaningful boundaries:

- Session start / pause / handoff;
- Prediction lock / comparison;
- scope amendment;
- blocker / contamination;
- natural checkpoint;
- acceptance / closure.

A compact Operational Recovery Checkpoint should preserve:

```text
Source / Revision identity
Session / scope / revealed position
latest precise locator
Profile / immutable prediction refs
stop boundary
blocker / finding
exactly one next action
```

Keep it separate from the richer ReadingSession Learning Artifact.

## Stop boundary

One “下一句 / 下一步” normally authorizes one bounded ReadingStep.

At completion:

```text
current locator recorded
stop_boundary recorded
next independent SourceUnit remains unrevealed
next_action explicit
STOP
```

Do not automatically start another SourceUnit, Session mode, Paper or Task.

## Failure conditions

Fail closed and persist a recoverable blocker / handoff when:

- required MCP is unavailable or invocation is rejected;
- PaperRevision / normalized identity conflicts;
- locator / cursor is stale;
- exact re-read cannot be completed safely;
- next unit crosses scope;
- future Source contamination occurs;
- bound Profile version cannot be recovered;
- repo rules and durable Session state conflict.

Do not substitute Web paper text, model memory, downstream analysis or fuzzy search.

## Completion condition

This Skill succeeds when it executes the current authorized ReadingSession action, preserves Source / scope / Profile / no-lookahead boundaries, writes required durable state, and stops.
