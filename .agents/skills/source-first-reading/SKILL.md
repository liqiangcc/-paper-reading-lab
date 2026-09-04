---
name: source-first-reading
description: Start, continue, resume, or safely pause a paper-reading-lab source-first ReadingSession using GitHub durable state and reading-mcp canonical Source. Use for “下一句/下一步”, sequential paper reading, fresh-conversation recovery, current-step fidelity review, or a ReadingSession blocker. Do not use for generic repository governance or unrelated paper summaries.
---

# Source-First Reading

## Role

This Skill executes one bounded ReadingSession action under the repository's existing protocol.

It does not redefine Source identity, no-lookahead, ReadingSession lifecycle, Explanation Profile, or Issue workflow. Those remain canonical in repository docs.

## Required tools

Use:

```text
github-mcp
→ live Issue / PR / durable control state

reading-mcp
→ canonical paper Source / SourceUnit / TextLocator / source view
```

Do not use Web to obtain or search the paper body during a clean first-pass source-first Session when `reading-mcp` is the bound Source provider.

## Mandatory bootstrap

Before Source reveal:

1. Read root `AGENTS.md`.
2. Read the target Issue live state and relevant comments.
3. Read `docs/workflows/conversation-bootstrap.md`.
4. Recover the latest applicable checkpoint / handoff / blocker / next_action.
5. Read these canonical method docs as needed:
   - `docs/learning/source-first-sentence-reading.md`
   - `docs/learning/reading-sessions.md`
   - `docs/workflows/paper-reading-lifecycle.md`
   - `docs/workflows/issue-driven-workflow.md`
   - `docs/validation/invariants.md`
6. If durable state binds an Explanation Profile, read exactly the bound `style_profile.source` and version. Do not silently use a newer Profile.

Do not require the user to re-paste locator, Profile rules, or old transcript when durable GitHub state already contains them.

## Recover execution state

Before doing anything irreversible or revealing new Source, recover and verify:

```text
paper_id
revision_id
reading provider
reading_document_id / normalized identity
Session mode
lookahead policy
planned_scope
current_scope_boundary
revealed_position
latest precise TextLocator
bound Profile id/version/source (if any)
immutable prediction reference (if any)
next_action
```

If critical state is missing or conflicting, fail closed. Do not reconstruct it from model memory.

## Scope gate before reveal

Every new canonical reveal must be preceded by a scope check.

```text
current locator
→ determine whether the next canonical unit is inside current_scope_boundary
→ inside?
   ├─ yes → reveal is allowed
   └─ no  → STOP before Source is revealed
             ↓
          durable scope amendment required
```

Never reveal first and amend scope afterwards.

## Canonical sequential reveal

For ordinary sentence-first reading, default to exactly one canonical SourceUnit:

```text
get_text_units(
  requested_kind = sentence,
  direction = forward,
  coverage_policy = preserve_source,
  max_items = 1
)
```

Anchor at the latest precise locator from durable state or the current conversation's revealed position.

If the returned unit is structural / non-prose / code / figure label, follow the current protocol and scope boundary one canonical unit at a time. Do not batch-read future text merely to find something “more useful”.

If segmentation splits one semantic sentence, preserve canonical fragments and the existing reveal-group rules. Never hide source degradation by inventing a new sentence identity.

## Exact re-read

For the allowed returned unit, use precise locator re-read:

```text
read_document(document_id, target_locator)
```

Do not fuzzy-search old snippets to recover a stale locator.

If exact re-read returns stale / identity mismatch / invocation failure:

```text
fail closed
→ do not fetch a second unit
→ persist blocker / handoff if this is a durable boundary
→ STOP
```

## Original-source fidelity

Use `get_source_view` only when the **current allowed Source** requires visual verification, such as:

- Figure;
- Table;
- Equation;
- Algorithm;
- multi-column layout;
- parser-fidelity ambiguity.

Keep separate:

```text
text Source Fact
vs
original-page visual observation
```

Seeing a whole page does not authorize use of future text on that page in a clean no-lookahead Session.

## Explanation

If a formal Explanation Profile is bound, follow it exactly by `id + version + source`.

If no formal Profile is bound, use the minimum Source-First structure without assuming the latest Profile:

```text
canonical original
→ faithful translation / literal meaning as applicable
→ relation to revealed past
→ actual cognitive increment
→ current problem model update
→ Source Fact / Derived / Unknown boundary
→ precise locator
→ STOP
```

Every explicit reasoning arrow must be traceable to revealed Source or remain explicitly Derived.

Do not inject modern implementation details or future sections into historical paper interpretation.

## Stop boundary

One user “下一句 / 下一步” normally authorizes one bounded ReadingStep, not an unlimited reading loop.

At the end of the Step:

```text
save / report current precise locator
save stop_boundary
next independent SourceUnit remains unrevealed
STOP
```

Do not automatically start another SourceUnit, another Session mode, another paper, or another Task.

## Durable writes

Do **not** copy every long sentence explanation into the Primary Issue.

Write durable GitHub state at meaningful boundaries, including:

- Session start / pause / handoff;
- Prediction lock;
- scope amendment;
- blocker;
- natural checkpoint;
- acceptance / closure.

A durable handoff should be operational and compact. It should contain enough to restore safe execution, not a full transcript.

If the current Issue protocol separates Operational Recovery Checkpoint and ReadingSession Learning Artifact, preserve that separation.

## Prediction rule

When the current mode counts a Prediction as training evidence:

```text
persist prediction
→ only then reveal actual next SourceUnit
→ append comparison
```

Never edit the original prediction after reveal to make it appear more accurate.

## Failure rules

Stop and persist a blocker / handoff when any of these occur:

- required MCP unavailable or invocation rejected;
- PaperRevision / normalized identity conflict;
- stale locator / cursor;
- exact re-read failure that cannot be safely retried without changing Source scope;
- next unit would cross `current_scope_boundary`;
- future Source contamination;
- bound Profile version cannot be recovered;
- canonical repo rules conflict with durable Session state.

Do not substitute model memory, Web paper text, downstream analysis, or fuzzy search to keep moving.

## Thin-entry success condition

This Skill is working as intended when a fresh conversation can receive only:

```text
repo + Issue + “read AGENTS.md and execute by repository governance”
```

and then recover all necessary ReadingSession state from GitHub + canonical repo docs + `reading-mcp` without the user re-pasting the old long prompt.

## Core invariants

```text
GitHub durable state controls workflow.
reading-mcp controls paper Source truth.
Canonical repo docs control method.
A bound Profile controls presentation, not Source visibility.
Scope is checked before reveal.
Exactly-one is the default ReadingStep reveal size.
Precise locator failure fails closed.
Current explanation cannot depend on future Source.
Current Step ends at an explicit stop boundary.
```
