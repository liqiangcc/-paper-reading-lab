# Agent Working Rules

## 1. Repository purpose

`paper-reading-lab` governs source-grounded paper learning:

```text
Paper / PaperRevision identity
ReadingSourceBinding
ReadingSession / scope / checkpoint
Source-first / no-lookahead learning
Prediction / Recall / Reconstruction / Transfer
Explanation Profile
Issue-driven durable control state
```

It does not parse papers or own canonical SourceUnit identity. `reading-mcp` is the preferred Source Adapter and source truth for document structure, SourceUnit, TextLocator and original-source view.

## 2. Thin-entry bootstrap

For Issue-driven work, start in this order:

```text
read AGENTS.md
→ read target Issue live state + relevant comments
→ identify latest applicable durable record / next_action
→ read docs/workflows/conversation-bootstrap.md
→ route to an applicable Skill
→ load only the canonical docs required for that action
→ execute the authorized bounded action
→ persist result / blocker / handoff
→ STOP
```

Do not require the user to re-paste state already present in GitHub durable records.

## 3. Skill routing

Use [`.agents/skills/source-first-reading/SKILL.md`](.agents/skills/source-first-reading/SKILL.md) when the task is to:

- start, continue or resume a source-first ReadingSession;
- execute “下一句 / 下一步” sequential reading;
- recover from a ReadingCheckpoint / `[SESSION HANDOFF]`;
- perform fidelity review for the current allowed Figure / Table / Equation;
- stop safely on scope, locator, revision, Profile or MCP failure.

Do not use that Skill for generic repository audits, governance edits, unrelated summaries, PR review or Task implementation that does not enter a ReadingSession.

When no Skill applies, follow the relevant canonical workflow docs directly. Do not force-fit a Skill.

## 4. Canonical method sources

Treat these as method truth:

```text
docs/architecture/boundaries.md
docs/domain/model.md
docs/integrations/reading-mcp.md
docs/source/source-policy.md
docs/learning/source-first-sentence-reading.md
docs/learning/incremental-explanation-profile.md
docs/learning/reading-sessions.md
docs/workflows/issue-driven-workflow.md
docs/workflows/paper-reading-lifecycle.md
docs/validation/invariants.md
```

Use [`docs/README.md`](docs/README.md) for navigation.

If a Session binds an Explanation Profile, load the exact `profile_id + version + source` from durable state. Never silently substitute the latest Profile.

Static docs do not define live task state. Current Paper / Session / Task state comes from the target Issue's latest applicable durable record.

## 5. Tool boundaries

```text
github-mcp
= repository / Issue / PR live state and durable control plane

reading-mcp
= paper Source, canonical structure, SourceUnit, TextLocator, source view

Web
= external public research only when explicitly allowed
```

For a clean first-pass source-first Session, do not use Web, downstream analysis, Issue prose or model memory to obtain future paper body text.

Tool availability must be proven by actual invocation when required. A schema, release note or previous conversation is not live evidence.

## 6. Reading invariants

For a clean no-lookahead Session:

- current explanation uses only revealed past + current allowed Source;
- `planned_scope` is durable history;
- `current_scope_boundary` is checked before every new reveal;
- crossing scope defaults to STOP until a durable amendment exists;
- `revealed_position` moves monotonically forward;
- precise continuation uses provider identity and TextLocator;
- stale locator / cursor or identity mismatch fails closed;
- future Source is not supplied early merely because the model promises not to use it;
- Prediction is persisted before actual reveal when counted as training evidence;
- a bound Profile controls presentation, not Source visibility;
- Session recovery does not silently switch PaperRevision or Profile version.

## 7. Source / Derived boundary

Always keep distinguishable:

```text
Source Fact
Derived Interpretation
Unknown
```

Generated reconstruction never becomes Source wording. Persisted explicit reasoning links must be traceable to revealed Source or remain explicitly Derived.

Original-page visual observation is also distinct from extracted text Source Fact and AI visual interpretation.

## 8. Durable state

GitHub Issue is the long-lived control plane, not the paper Source, full transcript or complete learning database.

Persist at meaningful boundaries:

- Session start / pause / handoff;
- Prediction lock / comparison;
- scope amendment;
- blocker / contamination;
- natural checkpoint;
- acceptance / closure.

Do not write every long sentence explanation into the Primary Issue.

Keep separate:

```text
Operational Recovery Checkpoint
≠ ReadingSession Learning Artifact
≠ Primary Issue summary
≠ full transcript
```

## 9. Failure behavior

When required capability is unavailable, Source identity is stale, exact re-read fails, scope would be crossed, bound Profile cannot be recovered, or canonical rules conflict:

```text
fail closed
→ do not infer / fuzzy-rebase / use memory to continue
→ persist blocker + recoverable handoff when needed
→ STOP
```

If future Source is exposed, record contamination. Do not continue claiming a clean first-pass Session.

## 10. Repository changes

Method, workflow, governance and validator changes must be Issue-driven and reviewed through an isolated branch / PR.

Before changing canonical docs:

- read the target Issue and relevant live state;
- check for overlapping open PRs;
- preserve historical Session facts;
- avoid writing transient “current task” claims into stable docs;
- run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate_repository.py` when available;
- record exact Candidate SHA and actual evidence;
- do not claim checks that were not run;
- before Task closure follow [the closure evidence gate](docs/workflows/issue-driven-workflow.md#task-closure-证据门禁), then re-read body/state/owner.

Repository governance stays layered:

```text
AGENTS.md
= routing + hard invariants

Bootstrap
= recovery algorithm

Skill
= bounded executable procedure

Canonical docs
= detailed method truth
```

## 11. Stop conditions

Stop after the authorized action is complete or blocked. Do not automatically:

- reveal another independent SourceUnit;
- expand Session scope;
- start another Session or Paper;
- merge or close unrelated Tasks;
- promote a Pilot candidate to stable without its acceptance evidence.
