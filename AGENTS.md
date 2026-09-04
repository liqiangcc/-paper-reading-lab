# Agent Working Rules

## 1. Repository purpose

`paper-reading-lab` governs source-grounded paper learning: Paper / PaperRevision identity, ReadingSession state, no-lookahead learning, Prediction / Recall / Reconstruction, durable checkpoints, and Issue-driven control.

It does **not** own PDF parsing or canonical SourceUnit identity. `reading-mcp` is the preferred Source Adapter and source truth for document structure, SourceUnit, TextLocator, and original-source view.

## 2. Thin-entry bootstrap

For Issue-driven work, a thin prompt should be sufficient if durable state is complete.

Start in this order:

```text
read AGENTS.md
→ read target Issue live state + all relevant comments
→ locate latest durable checkpoint / handoff / blocker / next_action
→ read docs/workflows/conversation-bootstrap.md
→ route to the relevant Skill
→ load only the canonical docs required by that Skill
→ execute the allowed next action
→ persist result / blocker / handoff
→ STOP
```

Do not rely on old ChatGPT conversation state when GitHub durable state is available.

## 3. Skill routing

Use `.agents/skills/source-first-reading/SKILL.md` when the task is any of:

- start a source-first ReadingSession;
- continue / “下一句” / “下一步” sequential reading;
- resume from a ReadingCheckpoint or `[SESSION HANDOFF]`;
- execute one ReadingStep under a bound Explanation Profile;
- perform Figure / Table / Equation fidelity review for the current allowed Source;
- stop safely at scope / locator / runtime blockers.

Do not use the reading Skill for generic repository governance, unrelated documentation work, or retrospective paper summaries unless the task explicitly enters a ReadingSession.

## 4. Canonical method sources

Repository agents should treat these as canonical method documents:

```text
docs/architecture/boundaries.md
docs/integrations/reading-mcp.md
docs/learning/source-first-sentence-reading.md
docs/learning/reading-sessions.md
docs/workflows/issue-driven-workflow.md
docs/workflows/paper-reading-lifecycle.md
docs/validation/invariants.md
```

If the current Session binds an Explanation Profile, load the exact `style_profile.source` and version from durable state. Never silently substitute the latest Profile.

`docs/README.md` is the navigation entrypoint for additional documents.

## 5. Tool boundaries

```text
github-mcp
= Issue / PR / repository live state and durable control plane

reading-mcp
= paper Source, canonical structure, SourceUnit, TextLocator, original source view

Web
= public external research only when explicitly allowed
```

For first-pass source-first reading, do not use Web to obtain or search the paper body when the canonical Source is bound through `reading-mcp`.

Issue comments, model memory, downstream analysis, OCR reconstruction, or visually observed future page text are not substitutes for canonical Source reveal.

## 6. Reading invariants

For a clean no-lookahead ReadingSession:

- Current explanation may use only revealed past + current allowed Source.
- `revealed_position` moves monotonically forward.
- `current_scope_boundary` is checked **before** each new canonical reveal.
- Crossing scope defaults to STOP until a durable scope amendment exists.
- Precise continuation uses provider identity / TextLocator; stale identity fails closed.
- Future Source must not be supplied early merely because the model promises not to use it.
- Prediction must be persisted before actual reveal when it is being counted as Prediction evidence.
- A bound Explanation Profile cannot expand Source visibility.
- Session recovery must not silently switch PaperRevision or Profile version.

## 7. Source / Derived boundary

Always distinguish:

```text
Source Fact
Derived Interpretation
Unknown
```

Generated reconstruction never becomes Source wording. Every persisted explicit reasoning link should be traceable to revealed Source or remain explicitly Derived.

## 8. Durable state

GitHub Issue is the long-lived control plane, not the paper Source, full transcript, or complete learning database.

Persist durable state at meaningful boundaries such as:

- Session start / pause / handoff;
- Prediction lock;
- scope amendment;
- blocker;
- natural checkpoint;
- acceptance / closure.

Do not write every long sentence explanation into the Primary Issue.

Operational Recovery Checkpoint and ReadingSession Learning Artifact remain separate concerns.

## 9. Failure behavior

If required MCP capability is unavailable, Source identity is stale, exact locator re-read fails, scope would be crossed, or canonical rules conflict:

```text
fail closed
→ do not infer / fuzzy-rebase / use memory to continue
→ persist blocker + recoverable handoff
→ STOP
```

## 10. Repository changes

Method / workflow / governance changes should be Issue-driven and reviewed through a branch / PR. Do not silently rewrite historical Session state to match new protocol versions.

Keep repository governance thin: AGENTS.md routes and protects invariants; canonical docs carry detailed method; Skills carry executable procedures.
