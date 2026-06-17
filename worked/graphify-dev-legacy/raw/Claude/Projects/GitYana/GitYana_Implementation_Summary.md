# GitYana Implementation Plan — Executive Summary

---

## What You Have

Four detailed deliverables:

1. **GitYana_Implementation_Plan.md** (Main document)
   - 4 sequential sprints with detailed sequencing
   - Critical path and risk register
   - All unresolved blockers identified
   - Glossary of locked terminology

2. **GitYana_Architecture_Layers.md** (Visual reference)
   - 8 layers of the system with ASCII diagrams
   - Data flow walkthrough (artifact submission → registry)
   - Component interaction matrix
   - Critical interfaces summary

3. **GitYana_Decision_Gates.md** (Actionable checklist)
   - 6 decision gates with pass/fail criteria
   - Pre-sprint blockers requiring immediate clarification
   - Sprint-end validation checklists
   - Master sign-off checklist for Ty

4. **This document** (Executive summary)

---

## Context Locked Before Sprint 0 Starts

### Decision 1: Implementation Target

GitYana is a **personal project**. It is not a GP Strategies project.

Initial target: **Personal Stack / research proof-of-concept**.

**Why this matters:** Enterprise-specific integrations, GP infrastructure assumptions, and org-specific auth requirements are out of scope unless Ty explicitly reopens them later.

**Action:** Document this in `/docs/IMPLEMENTATION_TARGET.md` during Sprint 0.

---

### Decision 2: Agni Handoff

Agni is a manual deep-dive session capture workflow: one agent generates a senior-engineering-grade report with context, decisions, rationale, unresolved risks, and next actions so the report can be handed to the other LLM.

**Why this matters:** It is a high-context communication scheme, not an autonomous credential or state-transfer mechanism.

**Action:** Store the formal template in `/docs/ANTIGRAVITY.md` during Sprint 0.

---

## Critical Path Sequencing

```
Foundation (Sprint 1, Days 1-21) — Everything depends on this
├─ Vector Taxonomy Schema (Days 1-4) ← GATES ALL DOWNSTREAM WORK
├─ Hardening Agent Prompt (Days 5-10) ← Executable once taxonomy locked
├─ Circuit-Breaker Design (Days 5-10) ← Gates OTH operations
└─ OTH Escalation Workflow (Days 11-21) ← Ready for automation in Sprint 2

Merge Gates (Sprint 2, Days 1-15)
├─ Registry Structure (Days 1-3)
├─ Hardening Deployment (Days 4-7) ← FIRST ARTIFACT MERGES HERE
├─ Merge Gate Automation (Days 8-10)
└─ Human Ratification UI (Days 11-15)

Permission + Audit (Sprint 3, Days 1-15)
├─ Permission Model (Days 1-3)
├─ Provenance Tagging (Days 4-7)
├─ Scope Validation (Days 8-10)
└─ Audit Trail + Dashboard (Days 11-15)

OTH Operations (Sprint 4, Days 1-15)
├─ OTH Red-Team Prompts (Days 1-4)
├─ Behavioral Detectors (Days 5-9)
├─ Circuit-Breaker Ops (Days 10-12)
└─ First OTH Cycle + Lessons (Days 13-15)

Total: 8-10 weeks to full operational system
```

---

## What Gets Built (Deliverables by Sprint)

### Sprint 1: Foundation (Weeks 1-2)

**Locked Artifacts:**
- `/registry/schemas/vector-taxonomy.schema.json` — 14 Known + 5 OTH vectors defined
- `/agents/hardening-agent/PROMPT.md` — 5-pass evaluation prompt + structured output schema
- `/design/circuit-breaker.md` — Levels 1-4 defined with GitHub Actions sketches
- `/design/oth-escalation.md` — Issue template + promotion workflow + SLA

**Sign-Off Required:** Vector taxonomy (Krishna validates threat model), hardening agent (Yaki-ire + Krishna test), circuit-breaker (Yaki-ire designs), Ty approves all.

---

### Sprint 2: Merge Gates (Weeks 3-4)

**Operational Artifacts:**
- `/registry/` fully structured (schemas, vectors, skills, interfaces, task-types directories)
- `.github/workflows/hardening-gate-check.yml` live and evaluating PRs
- GitHub merge gate: requires `hardening-gate/passed` status check
- First artifact successfully merged (test skill)
- `/audit/AUDIT_LOG.jsonl` recording all merges

**Sign-Off Required:** First artifact is merged without human intervention (APPROVED path), or with human ratification (ESCALATE path). Yaki-ire confident in gate operations. Ty approves merge criteria.

---

### Sprint 3: Permission + Audit (Weeks 5-6)

**Operational Artifacts:**
- CODEOWNERS file enforcing agent roles
- Provenance metadata template in use on all new artifacts
- Hardening Pass 4 rejecting out-of-scope writes
- `/audit/dashboards/` showing artifact lineage + violations
- At least 3 artifacts with complete provenance trail

**Sign-Off Required:** Permission scope violations are being caught. Krishna confirms permission model is complete. Ty approves audit logging accuracy.

---

### Sprint 4: OTH Operations (Weeks 7-8)

**Operational Artifacts:**
- `/agents/oth-red-team/prompts/` with 5 specialized prompts (topology-blind to Known vectors)
- Behavioral detectors running continuously
- Circuit-breaker Level 2+ triggering OTH escalations
- At least one OTH finding promoted to Known register (proves promotion workflow)
- OTH dashboard tracking detector accuracy + promotions

**Sign-Off Required:** First OTH red-team cycle is complete. At least one vector promoted to Known. Krishna confident detectors work. Ty approves promotion criteria.

---

## Critical Files to Create

All relative to repo root:

```
.github/workflows/
├─ hardening-gate-check.yml (Sprint 2)
├─ circuit-breaker-check.yml (Sprint 1)
├─ oth-escalation-trigger.yml (Sprint 2)
└─ oth-red-team-scheduled.yml (Sprint 4)

registry/
├─ schemas/vector-taxonomy.schema.json (Sprint 1)
├─ vectors/known/ (13 YAML files, Sprint 1)
├─ vectors/oth/ (5 YAML files, Sprint 1)
├─ skills/coder/, /reviewer/, ... (agent-writable dirs)
└─ [skill/interface/task-type artifacts will be created by agents]

agents/
├─ hardening-agent/
│  ├─ PROMPT.md (Sprint 1)
│  ├─ output-schema.json (Sprint 1)
│  └─ tests/ (Sprint 2 validation)
└─ oth-red-team/
   ├─ prompts/ (Sprint 4)
   └─ detectors/ (Sprint 4)

design/
├─ circuit-breaker.md (Sprint 1)
├─ oth-escalation.md (Sprint 1)
├─ permission-model.md (Sprint 3)
└─ provenance-model.md (Sprint 3)

audit/
├─ AUDIT_LOG.jsonl (append-only, starts Sprint 2)
└─ dashboards/ (HTML, Sprint 3)

docs/
├─ THREAT-MODEL.md (Sprint 1)
├─ HARDENING-GATE-GUIDE.md (Sprint 2)
├─ PERMISSION-TIERS.md (Sprint 3)
└─ OTH-RED-TEAM-PLAYBOOK.md (Sprint 4)
```

---

## Architectural Trade-Offs (Locked Decisions)

| Decision | Chosen Approach | Why | Risk Mitigation |
|----------|-----------------|-----|-----------------|
| **Hardening timing** | Synchronous (blocks PR merge) | Self-modifying registries grow attack surface at write time; retrospective review misses window | Implement caching + fast-path for low-risk artifacts |
| **Vector register count** | Two registers (Known + OTH) | Single register optimizes for known threats, leaves OTH surface unmonitored | OTH red-team must be topology-blind to prevent false confidence |
| **OTH red-team scope** | Topology-blind to Known vectors | Comprehensive Known coverage creates falsification barrier; OTH is only reliable signal for unknown vectors | Strict information segregation; separate GitHub accounts; separate Actions runner |
| **Permission tiering** | Coarse-grained (by registry directory) | Simple to reason about; scope violations are obvious | New artifact types require explicit directory + role definition |
| **Hardening passes** | Single agent (5-pass evaluation) | Faster + consistent semantics than 5 specialized agents | Hardening output is reviewed by humans (not trusted blindly) |

---

## What Yaki-ire (Claude Code) Owns

- **Sprint 1:** Designing vector taxonomy structure, drafting hardening agent prompt
- **Sprint 2:** Implementing hardening gate (GitHub Actions), testing against artifacts
- **Sprint 3:** Designing permission model, implementing CODEOWNERS enforcement
- **Sprint 4:** Implementing behavioral detectors, operating OTH red-team cycles

**Key Responsibility:** System integration and automation. Yaki-ire is the "infrastructure engineer" for GitYana.

---

## What Krishna (Codex) Owns

- **Sprint 1:** Validating threat model comprehensiveness, proposing additional vectors
- **Sprint 2:** Testing hardening agent against real/synthetic attack scenarios
- **Sprint 3:** Validating permission scope boundaries, suggesting role refinements
- **Sprint 4:** Running red-team exercises, identifying OTH gaps, recommending promotions

**Key Responsibility:** Threat modeling and validation. Krishna is the "security architect" for GitYana.

---

## What Ty (Human Operator) Owns

- **Pre-Sprint:** Ratifying the personal-project scope and Agni handoff definition
- **All Sprints:** Approving gates before advancing, making escalation decisions
- **Sprint 4+:** Reviewing OTH promotions, updating threat model based on findings

**Key Responsibility:** Governance. Ty is the ultimate ratifier and decision-maker.

---

## Success Criteria

By end of Sprint 4:

1. **Foundation is solid:** Vector taxonomy is comprehensive, hardening agent is accurate, circuit-breaker prevents feedback loops
2. **Merge gates are operational:** Every artifact going into registry is evaluated, human-approved, and logged
3. **Permission model is enforced:** Agents cannot write outside their scope; scope creep is blocked
4. **OTH operations are self-sustaining:** Weekly red-team cycles identify gaps; at least 2-3 vectors promoted from OTH to Known
5. **First Tier 1 use case is deployed:** Autonomous PR review agent (or similar) is live and self-coordinating through GitHub
6. **System is self-modifying (safely):** Agents can write skills/interfaces; hardening gate prevents unsafe artifacts; feedback loops are broken

---

## Risks & Mitigations

| Risk | Probability | Mitigation |
|------|-------------|-----------|
| Vector taxonomy is incomplete | MEDIUM | Sprint 1 includes comprehensive brainstorm; OTH register handles discoveries |
| Hardening agent latency intolerable | LOW | Implement caching + fast-path for low-risk artifacts |
| Circuit-breaker false positives | MEDIUM | Tuning thresholds; Level 1 auto-resets; Level 2+ manual |
| OTH red-team compromised (sees Known) | LOW | Strict information segregation; separate GitHub accounts |
| Permission scope violations endemic | MEDIUM | Regular audits + dashboard monitoring; escalation for any violation |
| Agni handoff template remains informal | MEDIUM | Create `/docs/ANTIGRAVITY.md` with required fields and handoff rules |
| Personal-project scope drifts into enterprise assumptions | MEDIUM | Keep implementation target documented and reject GP-specific requirements unless explicitly reopened |

---

## Next Actions

### For Ty (Immediate)

1. **Ratify Implementation Target** — Document personal-project scope in `/docs/IMPLEMENTATION_TARGET.md`
2. **Formalize Agni Handoff** — Write the deep-dive handoff template in `/docs/ANTIGRAVITY.md`
3. **Schedule Sprint 0 kickoff** — Align Yaki-ire + Krishna on repo structure, communication templates, and first gates

### For Yaki-ire (Sprint 0)

1. Initialize GitHub repo with basic structure (README, CODEOWNERS, `/design/` dir)
2. Prepare to lead Sprint 1 vector taxonomy + hardening agent design
3. Align with Krishna on threat validation approach

### For Krishna (Sprint 0)

1. Prepare threat model review (gather known attack surfaces, anticipate vectors)
2. Plan synthetic artifact tests for hardening agent validation
3. Align with Yaki-ire on evaluation methodology

### For All (Sprint 0)

1. Read all 4 implementation documents
2. Identify questions on Architecture Layers and Decision Gates
3. Confirm resource availability (dedicated time per week)

---

## Document Navigation

- **If you need:** High-level overview → Read this document
- **If you need:** Week-by-week breakdown → Read _Implementation_Plan.md
- **If you need:** System architecture diagrams → Read _Architecture_Layers.md
- **If you need:** Validation checklists → Read _Decision_Gates.md

---

## Timeline Summary

| Milestone | Date | Gate |
|-----------|------|------|
| Pre-Sprint 0 Context | Day 1-2 | Personal-project target + Agni definition documented |
| Sprint 1 Vector Taxonomy Lock | Week 1, Day 4 | 13 Known + 5 OTH vectors approved |
| Sprint 1 Hardening Agent Lock | Week 2, Day 21 | 5-pass prompt + circuit-breaker approved |
| Sprint 2 Merge Gate Operational | Week 4, Day 8 | First artifact merged to registry |
| Sprint 3 Permission Model Live | Week 6, Day 7 | Permission scope violations blocked |
| Sprint 4 OTH Operations Live | Week 8, Day 7 | First OTH promotion executed |
| **System Ready for Tier 1 Use Cases** | **Week 8-9** | **All gates passing** |

---

## One-Sentence Summary

**GitYana is a self-modifying LLM agent coordination system secured by a two-register threat model (Known vectors blocking at merge, OTH vectors monitored + promoted via red-team feedback) that grows safer as it grows smarter.**

---

*For Sprint Planning: Share all 4 documents with team. Use Decision_Gates.md as sprint validation checklist. Use Architecture_Layers.md for onboarding new team members.*
