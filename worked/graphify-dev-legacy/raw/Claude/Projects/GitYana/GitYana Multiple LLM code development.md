GitYana: Multiple LLM code development and coordination thru a GitHub repo

# ENGINEERING TEAM DEV NOTES
**Project:** GitYana: Multiple LLM code development and coordination thru a GitHub repo
**Session Date:** 2026-05-31
**Compiled by:** Claude Sonnet 4.6
**Status:** Active / Pre-implementation -- architecture design phase

---

## 1. PROBLEM STATEMENT & ORIGIN FRAMING

The session opened with a question about virtualized API channels spun up between two or more LLMs, coordinated through GitHub, covering coding, review, main branch updates, and task allocation.

Initial architecture interpretation established:

- Two or more LLM instances (same or different models)
- GitHub as the shared state machine / message bus / task registry
- LLMs do not communicate peer-to-peer directly -- GitHub is the intermediary
- GitHub primitives used as coordination protocol: Issues, PRs, branches, Actions, comments, webhooks

---

## 2. TIER 1 USE CASES -- HIGH SIGNAL, NEAR-DEPLOYABLE

**2.1 Autonomous PR Review Loop**
Agent A writes code and opens a PR. Agent B (specialized: security, style, logic) is triggered by webhook. B comments directly on the diff. A reads comments, revises, pushes new commit. Merge gate requires B's approval. No human in loop until escalation threshold is hit.

**2.2 Spec-to-Code-to-Test Triangle**
Three agents: Architect writes a structured Issue spec in markdown. Coder translates spec to implementation branch. Tester writes tests against the spec independently. All three reconcile via PR -- mismatches surface as failing tests before human review.

**2.3 Dependency Triage Agent**
Dependabot/Renovate opens update PRs at scale. LLM agent reads each PR, assesses breaking change risk against codebase via code search, labels by risk tier, auto-merges low-risk patches, drafts human escalation notes for breaking changes. GitHub handles the queue.

**2.4 Documentation Drift Detector**
Agent A monitors commits to `/src`. Agent B owns `/docs`. On every merge to main, docs agent diffs code changes against documented behavior, opens Issues for drift, auto-drafts doc update PRs for human approval.

---

## 3. TIER 2 USE CASES -- STRUCTURALLY SOUND, NEEDS TOOLING INVESTMENT

**3.1 Multi-Agent Refactor Coordinator**
Large refactor broken into GitHub Issues tagged by module. Task allocation agent reads dependency graph, assigns Issues to coder agents in safe topological order (no agent touches a file another agent has checked out). Merge conflicts become failure signals -- coordinator detects and re-routes.

**3.2 Red Team / Blue Team Security Loop**
Blue agent writes feature code. Red agent is specifically prompted to attack it -- injection vectors, logic flaws, auth bypasses -- and files Issues as "attack reports." Blue agent required to resolve each before PR can merge. GitHub Issues function as the vulnerability register.

**3.3 Multi-Model Consensus Gate**
High-stakes changes (schema migrations, API contracts) require sign-off from N different LLMs (GPT-4, Claude, Gemini, or specialized models). Each reviews independently, posts structured approval/rejection comment. Merge workflow requires quorum. Divergence flags human review.

**3.4 Living Architecture Decision Record (ADR) Agent**
Monitors all PRs and commits for architectural decisions (new dependencies, pattern changes, structural shifts). Drafts ADR documents automatically, opens as PRs to `/docs/decisions`. Human approval required -- discovery and drafting are automated.

---

## 4. TIER 3 USE CASES -- HIGH LEVERAGE, LONGER FUSE

**4.1 Autonomous Bug Triage + Reproduction**
User-filed Issues hit GitHub. Triage agent classifies severity, attempts reproduction via test scaffolding, closes with reasoning if cannot reproduce, or escalates with a minimal reproduction case attached. Coder agent picks up escalated issues from labeled queue.

**4.2 Cross-Repo Consistency Enforcer**
For orgs with multiple repos sharing contracts (API schemas, shared libraries, config standards). Coordinator agent watches for changes in the contract repo, propagates required updates as PRs across all downstream repos tagged by urgency. Agents in each repo handle review.

**4.3 Synthetic Contributor for Knowledge Transfer**
When a senior dev's PRs reflect domain knowledge not in docs or tests, LLM agent reverse-engineers implicit knowledge into structured documentation and onboarding materials. GitHub blame + PR history is the input corpus.

---

## 5. ARCHITECTURE REGIME SHIFT -- THE KEY CONCEPTUAL BREAK

This is where the session moved beyond governance-on-GitHub into a fundamentally different model.

### 5.1 The Distinction That Must Stay Separated

**GitHub-as-coordination surface** (Tier 1-3 above): LLMs use GitHub's existing primitives as a shared state machine. The repo *is* the protocol.

**GitHub-as-build-surface** (what was established in this session): LLMs use GitHub to *fabricate new capability* -- generating skill packages, API adapters, planning modules, interface definitions -- and deploying those artifacts back into the coordination layer itself. The system is **writing its own tooling while running.**

GitHub becomes a **living registry of agent-authored extensions**, not just a message bus.

### 5.2 What the Self-Modifying Architecture Enables

**Self-expanding skill surface**
An agent hits a task it cannot complete with current tools. It writes a skill package (Python module, API wrapper, prompt template library), opens a PR to a `/skills` registry repo, a reviewer agent validates it, merged into shared tool pool. Next agent that hits the same gap pulls from the registry. Capability set grows without human authoring.

**Agent-authored interface contracts**
Two agents need to exchange structured data for a new task type. Neither has a defined schema. They negotiate a contract: one agent drafts OpenAPI or JSON Schema spec, opens as PR, other reviews and proposes amendments via comments. Merge = agreed contract. The interface emerges from the task rather than being pre-specified.

**Out-of-sandbox planning artifacts**
Agent encounters a task requiring external resources it doesn't have -- a new API, a data source, a human decision. Instead of failing silently, it generates a *capability gap document* as a GitHub Issue: what it needs, why, what it would build if it had access. That document becomes the handoff to either a human or another agent with broader permissions. The system maps its own blind spots.

**Dynamic task decomposition registry**
Planning agent breaks a novel task into subtasks it has never seen before, writes those subtask definitions as structured Issue templates into a `/task-types` registry, assigns them. Future planning agents inherit that decomposition pattern. The task ontology expands with use.

### 5.3 The Governance Flip

In the governance-on-GitHub model: humans define rules, agents operate within them.

In the self-modifying model: **agents are authoring the rules, the tools, and the interfaces.** GitHub is the append-only ledger that makes it auditable.

The governance question flips from "what can agents do?" to "what requires human ratification before an agent-authored artifact can execute?"

That is a **tiered write-permission problem, not a workflow problem.**

### 5.4 Required Architecture Components (from this session)

- Hard boundary between agent-writable registries and execution-gated registries
- Every agent-authored artifact tagged with provenance: which agent, which task context, what model version
- Human ratification as a merge gate on anything that expands agent permissions or touches external interfaces
- Drift detection on the registry itself -- agents can bloat or contradict the skill surface over time

---

## 6. HARDENING MODEL

### 6.1 Core Problem With Iterative Hardening as the Safety Model

Iterative review assumes the threat surface is stable between review cycles. In a self-modifying registry it is not. Every merged agent-authored artifact potentially introduces new attack surface *and* new review blind spots simultaneously.

The review loop cannot run at human speed or scheduled-batch speed. **It must be synchronous with the write cycle.**

### 6.2 Hardening as Merge Gate

Every artifact touching the execution-gated registry goes through a hardening agent *before* hitting human ratification. That agent runs a fixed threat model against the artifact -- a structured evaluation against a known vector taxonomy, not a general security scan. The taxonomy lives in a repo. Agents can propose additions. Human ratification required before new vectors enter the active threat model.

This gives:
- Hardening that scales with write velocity
- A versioned, auditable threat model that grows with the system
- Clear separation between known vector coverage and over-the-horizon gaps

### 6.3 Two-Register Threat Model

**Known Vectors Register** -- actively enforced at merge time:
- Hardcoded credentials or environment assumptions
- Relaxed input validation
- Implicit trust of upstream agent output without schema enforcement
- Permission scope creep (artifact requests broader access than task requires)
- Dependency injection of unvalidated external packages
- Prompt injection surface in any agent-authored template

**Over-the-Horizon (OTH) Register** -- monitored, not blocking:
- Candidate vectors identified but not yet formally modeled
- Stored as Issues, not gates
- A separate agent watches for behavioral signatures in merged artifacts that pattern-match to OTH candidates
- When a signature fires: escalates to human review, vector gets promoted to Known Register

The OTH register is where the real leverage is. Most systems don't have one.

### 6.4 Hardening Agent -- 5-Pass Evaluation Structure

For each artifact received:

**Pass 1 -- Static Analysis**
Known vector taxonomy check. Deterministic. Fast.

**Pass 2 -- Behavioral Intent**
What does this artifact *enable* that wasn't enabled before? Map the new capability surface delta.

**Pass 3 -- Interaction Surface**
Which other agents or registries does this artifact touch? Trace the dependency chain two hops out. Flag any node not hardened to the same standard.

**Pass 4 -- Scope Minimization**
Does this artifact request or assume permissions beyond what the originating task required? Flag any excess.

**Pass 5 -- Provenance Integrity**
Is the authoring agent operating within its defined task context? Off-context authorship is a signal, not automatically a block.

Output: structured report, not pass/fail. Human ratification gate sees the report alongside the artifact.

### 6.5 The Compounding Risk -- Falsification Barrier

Over time the known vector taxonomy gets comprehensive and the hardening agent gets good at it. That is exactly when exposure to novel vectors is highest -- the system has optimized for the threat model it has, and the attack surface it doesn't have modeled is the only viable entry point.

**Required: a scheduled adversarial red-team cycle explicitly NOT informed by the current taxonomy.** Its job is to ignore what the system knows and probe what it doesn't. Output goes to OTH register, not Known register. If it goes directly to Known, the signal about what the current model was missing is lost.

Key diagnostic question on fixed cadence: **"What would have to be true for our hardening model to be confidently wrong right now?"**

### 6.6 Primary Live Danger

The supply chain attack surface for agent-authored code. An agent writes a skill package that *works* but encodes a shortcut -- hardcoded credential, relaxed validation rule, implicit assumption about data shape. It passes review because the reviewer agent evaluates functional correctness, not second-order effects. That artifact is now in the shared registry and every subsequent agent inherits the flaw.

This is the **left-pad / log4j attack vector for agent-authored code, operating at machine write speed.**

---

## 7. ARCHITECTURE DECISIONS LOCKED THIS SESSION

| # | Decision | Rationale |
|---|---|---|
| 1 | GitHub plays two distinct roles -- coordination surface and build surface -- and these must stay architecturally separated | Conflating them removes the audit boundary |
| 2 | Hardening is a merge gate, not a scheduled batch audit | Self-modifying registries grow attack surface at write time -- retrospective review misses the window |
| 3 | Two-register threat model: Known Vectors (blocking) + OTH (monitoring + escalation) | Single-register models optimize for known threats, leave OTH surface unmonitored |
| 4 | OTH red-team cycle must be topology-blind to current taxonomy | Comprehensive known-vector coverage creates falsification barrier -- unknown surface becomes the only viable attack path |

---

## 8. OPEN THREADS -- PRIORITIZED BUILD QUEUE

| Priority | Thread | Notes |
|---|---|---|
| HIGH | Circuit-breaker design | Feedback loop prevention between agents that can both read/write Issues. No native GitHub circuit-breaker for agent activity -- must be explicit governance rule |
| HIGH | Vector taxonomy schema | Structure, fields, versioning, promotion workflow from OTH to Known. Everything else depends on this existing first |
| HIGH | Hardening agent instruction set | Full prompt + structured output definition for the 5-pass evaluation |
| HIGH | OTH escalation workflow | Trigger conditions, escalation path, human ratification gate design |
| HIGH | Permission tiering architecture | Agent-writable vs execution-gated registry boundary design |
| MED | Provenance/audit model | Tagging schema: agent identity, task context, model version |
| MED | Capability gap handoff pattern | Structured format for agent-authored gap documents as escalation artifacts |

---

## 9. RECOMMENDED BUILD ORDER

1. **Vector taxonomy schema** -- everything downstream depends on this structure existing
2. **Hardening agent instruction set** -- once taxonomy exists, 5-pass spec becomes a deployable prompt + structured output definition
3. **OTH escalation workflow + circuit-breaker** -- design together, they share the same governance surface and have overlapping trigger conditions. Designing separately creates a gap.
4. **Permission tiering + provenance model** -- load-bearing but can run in parallel or as second sprint

---

## 10. UNRESOLVED / REQUIRES DECISION BEFORE NEXT SPRINT

- **"Agni" handoff** -- referenced by Ty, context not resolved in this session. Likely a project codename, agent label, or Claude Code session. Must be clarified before handoff can execute.
- **Implementation target** -- architecture is currently conceptual. Three candidate targets: GP Strategies internal tooling, personal stack, or publishable framework. Answer changes spec fidelity requirements across the board.

### Follow-up Clarification

- **Implementation target resolved:** GitYana is a personal project. It is not a GP Strategies project.
- **Agni resolved:** Agni is a manual deep-dive session capture workflow used to pass senior-engineering-grade context, rationale, risks, and next actions between Yaki-ire and Krishna.
- **Planning implication:** Sprint 0 should document these decisions in repo artifacts instead of treating them as blockers.

---

*End of dev notes. Next session start with `/recap` or drop implementation target decision to unlock sprint 1.*
