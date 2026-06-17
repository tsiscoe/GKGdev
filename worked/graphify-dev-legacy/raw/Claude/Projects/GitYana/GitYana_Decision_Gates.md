# GitYana Implementation: Blocking Decision Gates

---

## GATE 0: PRE-SPRINT KICKOFF (REQUIRED BEFORE SPRINT 0 STARTS)

### Decision 1: Implementation Target

**Status:** Locked for Sprint 0.

GitYana is a **personal project**. The initial deployment model is a personal-stack research/proof-of-concept.

**Active Scope: Personal Stack** (Research, simplified constraints)
- SaaS-only: GitHub + Claude/Codex API + basic orchestration
- No enterprise integrations
- Generic threat model (no org-specific attacks)
- First merge gate operational: Week 2-3
- Owned by: Ty (personal experimentation)
- Rollout: Proof-of-concept, capability validation
- Fidelity required: MEDIUM (enough to prove the model works)

Enterprise/internal deployment and publishable-framework requirements are out of scope unless Ty explicitly reopens the target decision.

---

**Impact on Roadmap:**

| Aspect | Active Planning Constraint |
|--------|----------------------------|
| Vector taxonomy | Generic supply-chain, feedback-loop, permission, and prompt-injection risks |
| Hardening agent | Model-agnostic evaluation |
| Permission tiering | Simple Yaki-ire / Krishna / Ty authority boundaries |
| Integration testing | GitHub + local tooling first; API integrations only after gates are stable |
| Documentation | Practical project docs and templates |
| Sprint 1 Effort | Keep scope tight enough to prove the model before automation expands |

---

### Decision 2: Agni Handoff

**Status:** Defined for Sprint 0.

Agni is a manual deep-dive session capture workflow. It is used when one LLM needs to pass substantial project context, reasoning, decisions, risks, and next actions to the other LLM.

It is not currently treated as:

- A separate agent.
- A credential-transfer mechanism.
- A staging/live registry boundary.
- An enterprise/org boundary.

---

**Sprint 0 Action:** Create `/docs/ANTIGRAVITY.md` with the formal report template and required fields.

---

## GATE 1: SPRINT 0 COMPLETION (Day 2, Must Pass Before Sprint 1 Kickoff)

**Gate 1 Status as of 2026-06-14:** Signed off for Sprint 0 foundation by Ty. Remote `origin` is configured for `https://github.com/tsiscoe/GitYana.git`; remote/local history was reconciled; first push completed; current verified `origin/main` tip is `596fb80d9361968fea813781bbecc98f77ab2b7b`. GitHub-native coordination is usable for committed docs and messages, but protected operation still requires branch protection and remote-side governance settings.

**Audit Record:** See `/docs/GATE_1_CLOSURE.md` and `/docs/SPRINT_0_STATUS.md`.

### Checklist: Foundation Locked

- [x] **Implementation Target Documented:** Personal project / personal stack scope recorded
  - [x] Enterprise assumptions explicitly excluded
  - [x] Publishable-framework assumptions deferred

- [x] **Agni Handoff Documented:** Context fully understood
  - [x] Formal definition written and stored in `/docs/ANTIGRAVITY.md`
  - [x] Deep-dive report template created
  - [x] Permission implications documented

- [x] **Team Alignment:** Yaki-ire + Krishna + Ty have synced on:
  - [x] Implementation target and its constraints
  - [x] Agni coordination model
  - [x] Sprint 1 work division (Yaki-ire owns schemas/hardening, Krishna owns threat validation)
  - [x] Escalation path (Ty is final governance authority and resolves high-impact disagreement)

- [x] **Baseline Repo Created:** Local GitYana repository initialized
  - [x] README with target + high-level architecture
  - [x] `/design/` directory with architecture notes
  - [x] CODEOWNERS file (basic: `@tsiscoe` maintainer)
  - [x] CI/CD skeleton directory present with non-operational placeholder
  - [x] GitHub remote repository connected or created

**Sign-Off:** Ty requested explicit Gate 1 closure on 2026-06-12, provided the GitHub repository target `tsiscoe/GitYana` on 2026-06-13, explicitly signed off on 2026-06-13, and authorized repo coordination/push on 2026-06-14. This is recorded as approval of the Sprint 0 foundation and initial hub publication only. Protected GitHub-native operation remains blocked until branch protection is configured and remote-side governance settings are reviewed.

---

## GATE 2: SPRINT 1 VECTOR TAXONOMY LOCK (Day 4)

**Gate 2 Status as of 2026-06-13:** PASS. Ty approved all Gate 2 artifacts on 2026-06-13. Structural validation passed; formal JSON Schema/YAML parser validation remains recommended before enforcement automation depends on these files.

**Audit Record:** See `/docs/GATE_2_STATUS.md`, `/docs/THREAT-MODEL.md`, and `/docs/validation/GATE_2_VALIDATION.md`.

### Checklist: Vector Taxonomy Complete

- [x] **Schema Structure Drafted:** `/registry/schemas/vector-taxonomy.schema.json`
  - [x] JSON Schema draft accepted for Gate 2 based on JSON syntax and structural example checks; standards-compliant validator still recommended before automation
  - [x] Example vectors present and structurally checked
  - [x] Version field for taxonomy versioning (semantic)
  - [x] All required fields documented (vectorId, category, severity, detectionMethod, etc.)
  - [x] Extensible for new fields without breaking existing vectors

- [x] **14 Known Vectors Defined:** One `.yaml` file per vector in `/registry/vectors/known/`
  - [x] VECTOR-CREDS-001: Hardcoded credentials (with regex patterns)
  - [x] VECTOR-CREDS-002: Environment assumptions
  - [x] VECTOR-VAL-001: Unvalidated upstream output
  - [x] VECTOR-VAL-002: Relaxed validation in error paths
  - [x] VECTOR-UPST-001: Implicit trust without validation
  - [x] VECTOR-PERM-001: Permission scope creep
  - [x] VECTOR-PERM-002: Out-of-bounds registry writes
  - [x] VECTOR-DEPS-001: Unvetted external packages
  - [x] VECTOR-DEPS-002: Transitive dependency explosion
  - [x] VECTOR-PROMPT-001: Prompt injection (user input)
  - [x] VECTOR-PROMPT-002: Agent-authored template injection
  - [x] VECTOR-STATE-001: Shared state without locking
  - [x] VECTOR-REG-001: Registry pollution/duplication
  - [x] VECTOR-CAP-001: Capability creep without auth
  - [x] Each vector includes: name, description, severity, hardcoded checks (regex), example violation, required fix

- [x] **5 OTH Candidates Defined:** One `.yaml` file per candidate in `/registry/vectors/oth/`
  - [x] OTH-TIMING-001: Race conditions in parallel writes
  - [x] OTH-FEEDBACK-001: Unbounded Issue feedback loops
  - [x] OTH-MODEL-001: Model-specific assumptions
  - [x] OTH-ENUM-001: Permission boundary enumeration
  - [x] OTH-SUPPLY-001: Subtle supply-chain flaws
  - [x] Each OTH includes: description, potential impact, behavioral signature to watch for

- [x] **Threat Model Documentation:** `/docs/THREAT-MODEL.md`
  - [x] Explains why these 14 Known vectors (not fewer, not more)
  - [x] Explains OTH strategy (why topology-blind red-team matters)
  - [x] Documents any vectors considered but rejected (and why)

- [x] **Krishna Validation:**
  - [x] Krishna has reviewed threat model against known attack surfaces
  - [x] Krishna has proposed any additional vectors to add
  - [x] Krishna sign-off: "Threat model is provisionally comprehensive for initial Known register; Ty approved Gate 2 on 2026-06-13."

- [x] **Ty Approval:**
  - [x] Ty has reviewed all vectors
  - [x] Ty has approved schema structure
  - [x] Ty sign-off: "Vector taxonomy locked for hardening agent development"

**Gate Status:** PASS
- PASS → Unlock Sprint 1 Days 5-21
- FAIL → Iterate on vectors until approved

---

## GATE 3: SPRINT 1 HARDENING AGENT LOCK (Day 21)

**Gate 3 Status as of 2026-06-13:** Implemented for review. Not PASS until Yaki-ire, Krishna, and Ty sign-offs are complete.

**Audit Record:** See `/docs/GATE_3_STATUS.md`.

### Checklist: Hardening Agent Executable

- [x] **5-Pass Prompt Drafted:** `/agents/hardening-agent/PROMPT.md`
  - [x] Pass 1 (Static): Loads vector taxonomy, runs regex patterns, identifies violations
  - [x] Pass 2 (Intent): Parses artifact for new capabilities, maps capability delta
  - [x] Pass 3 (Surface): Traces dependencies, flags unhardened deps
  - [x] Pass 4 (Scope): Validates permissions against agent role
  - [x] Pass 5 (Provenance): Verifies signature + task context
  - [x] Prompt constrains output to structured JSON

- [x] **Output Schema Drafted:** `/agents/hardening-agent/output-schema.json`
  - [x] JSON Schema for evaluation report
  - [x] All passes produce structured output (not free-form text)
  - [x] Recommendation field: APPROVED | ESCALATE | BLOCKED
  - [x] Every violation references a vector ID (not loose descriptions)

- [x] **Synthetic Test Cases:** `/agents/hardening-agent/tests/`
  - [x] Test artifact with hardcoded secret (should trigger VECTOR-CREDS-001)
  - [x] Test artifact with out-of-scope permission request (should trigger VECTOR-PERM-001)
  - [x] Test artifact with unvalidated input (should trigger VECTOR-VAL-001)
  - [x] Test artifact with off-context authorship (should flag as signal in Pass 5)
  - [x] Test artifact that passes all passes (should output APPROVED)
  - [ ] For each test: manual evaluation confirms hardening agent output is correct

- [ ] **Yaki-ire Confidence:**
  - [ ] Yaki-ire sign-off: "Hardening agent prompt is ready for deployment"
  - [ ] Yaki-ire has tested all 5 passes against synthetic artifacts

- [x] **Krishna Validation:**
  - [x] Krishna has reviewed hardening prompt
  - [x] Krishna has run it against real-world attack scenarios (thought experiment)
  - [x] Krishna sign-off: "Hardening agent draft covers the initial known threat surface for review; deployment still requires Yaki-ire and Ty approval."

- [x] **Circuit-Breaker Design Drafted:** `/design/circuit-breaker.md`
  - [x] 4 levels defined with clear triggers
  - [x] GitHub Actions workflows sketched (not yet implemented)
  - [x] OTH integration point documented (Level 2+ → OTH escalation)

- [x] **OTH Escalation Workflow Drafted:** `/design/oth-escalation.md`
  - [x] Escalation Issue template defined (GitHub Issue form)
  - [x] Behavioral signature data fields documented
  - [x] Promotion decision criteria documented
  - [x] SLA for human review defined (30m for CRITICAL, 24h for MEDIUM, 5d for LOW)

- [ ] **Ty Approval:**
  - [ ] Ty has reviewed hardening agent prompt
  - [ ] Ty has approved circuit-breaker and OTH workflows
  - [ ] Ty sign-off: "Foundation layer is locked; ready for Sprint 2 implementation"

**Gate Status:** FAIL / PENDING KRISHNA AND TY APPROVAL
- PASS → Unlock Sprint 2 kickoff
- FAIL → Iterate on prompts/workflows until approved

---

## GATE 4: SPRINT 2 MERGE GATE OPERATIONAL (Day 8)

### Checklist: First Artifact Successfully Merged

- [ ] **Registry Repo Fully Structured:**
  - [ ] `/registry/schemas/` with all 4 schema files (vector-taxonomy, artifact, interface, task-type)
  - [ ] `/registry/vectors/known/` with all 14 vector YAML files
  - [ ] `/registry/vectors/oth/` with all 5 OTH YAML files
  - [ ] `/registry/skills/coder/`, `/registry/reviewer/`, etc. (agent-writable subdirs)
  - [ ] `/registry/interfaces/` and `/registry/task-types/` (shared artifact types)
  - [ ] CODEOWNERS file enforcing role-based write permissions

- [ ] **Hardening Gate Deployed:**
  - [ ] `.github/workflows/hardening-gate-check.yml` is live
  - [ ] Triggered on every PR creation to `/registry/`
  - [ ] Loads vector taxonomy from repo
  - [ ] Executes hardening agent (via LLM API call)
  - [ ] Posts evaluation report to PR comment
  - [ ] Sets GitHub status check: `hardening-gate/passed` or `hardening-gate/escalation-required` or `hardening-gate/failed`

- [ ] **Merge Gate Automation:**
  - [ ] Branch protection rule: require `hardening-gate/passed` status check
  - [ ] Human approval required if status is `escalation-required` (via `@gityana-admin approve` comment)
  - [ ] Auto-label artifacts by vector violations
  - [ ] Block BLOCKED artifacts (no merge path)

- [ ] **Human Ratification Workflow:**
  - [ ] Approval comment parser is working (detects `@gityana-admin approve`)
  - [ ] Approver is stored in audit trail
  - [ ] Merge happens automatically after approval

- [ ] **First Artifact Test:**
  - [ ] Yaki-ire submits test skill (markdown parser or similar)
  - [ ] Hardening agent evaluates it
  - [ ] Result is APPROVED (no violations)
  - [ ] PR is automatically merged to `/registry/skills/coder/`
  - [ ] Artifact is now live and usable

- [ ] **Audit Logging Started:**
  - [ ] Merge creates append-only audit record in `/audit/AUDIT_LOG.jsonl`
  - [ ] Record includes: artifact ID, agent, hardening result, human approval, timestamp

- [ ] **Yaki-ire Confidence:**
  - [ ] Yaki-ire sign-off: "Hardening gate is operational and working as expected"

- [ ] **Ty Approval:**
  - [ ] Ty has reviewed first merged artifact
  - [ ] Ty has verified audit trail is being created
  - [ ] Ty sign-off: "Merge gates are live; Sprint 3 can proceed"

**Gate Status:** PASS or FAIL
- PASS → Unlock Sprint 3 (Permission Model + Provenance)
- FAIL → Debug hardening gate latency / failures until working

---

## GATE 5: SPRINT 3 PERMISSION MODEL OPERATIONAL (Day 7)

### Checklist: Permission Tiering + Provenance Live

- [ ] **Agent Roles Defined in CODEOWNERS:**
  - [ ] Yaki-ire role: write to `/registry/skills/coder/`, read from `/registry/schemas/`
  - [ ] Krishna role: write to `/registry/interfaces/`, read from all `/registry/`
  - [ ] Additional specialist roles (if any, per implementation target)
  - [ ] Each role has explicit scope boundaries

- [ ] **Provenance Tagging Implemented:**
  - [ ] Artifact metadata template defined (JSON schema)
  - [ ] Every new artifact includes: createdBy (agent + model), taskContext, requiredPermissions, dependencies
  - [ ] Agent signature implementation (artifact is cryptographically signed with agent's private key)
  - [ ] Signature verification in hardening Pass 5

- [ ] **Scope Validation in Hardening Pass 4:**
  - [ ] Hardening agent checks: does artifact write to agent's assigned directory?
  - [ ] Hardening agent checks: does artifact request permissions beyond agent's role?
  - [ ] Violations trigger ESCALATE or BLOCKED (depending on severity)
  - [ ] At least 2 artifacts tested for scope violations (one should pass, one should fail)

- [ ] **Audit Infra Initialized:**
  - [ ] `/audit/AUDIT_LOG.jsonl` is append-only (GitHub prevents deletion)
  - [ ] Every artifact merge appends a record
  - [ ] Record includes: artifactId, actor, permissions used, timestamp, metadata hash
  - [ ] At least 3-5 artifacts logged

- [ ] **Dashboard Prototype:**
  - [ ] `/audit/dashboards/artifact-lineage.html` shows: creation → hardening eval → approval → merge
  - [ ] `/audit/dashboards/vector-violations.html` shows: violations per artifact type
  - [ ] Both dashboards are read-only (no write actions from dashboard)
  - [ ] Dashboard data is generated from AUDIT_LOG (not separate source)

- [ ] **Krishna Validation:**
  - [ ] Krishna has reviewed permission model for completeness
  - [ ] Krishna has tested scope violations (attempted cross-role writes)
  - [ ] Krishna sign-off: "Permission model is enforced; scope creep is blocked"

- [ ] **Ty Approval:**
  - [ ] Ty has reviewed all permissions
  - [ ] Ty has spot-checked audit trail accuracy
  - [ ] Ty sign-off: "Permission tiering + provenance are operational; Sprint 4 can proceed"

**Gate Status:** PASS or FAIL
- PASS → Unlock Sprint 4 (OTH Operations)
- FAIL → Iterate on permission definitions / audit logging until working

---

## GATE 6: SPRINT 4 OTH OPERATIONS LIVE (Day 7)

### Checklist: OTH Red-Team Cycle Completed

- [ ] **OTH Red-Team Prompts Written:** `/agents/oth-red-team/prompts/`
  - [ ] `supply-chain.md`: Inject subtle bugs that pass review
  - [ ] `feedback-loop.md`: Create unbounded Issues while evading circuit-breaker
  - [ ] `model-mismatch.md`: Exploit Claude vs GPT-4 differences
  - [ ] `permission-creep.md`: Gradually expand write scope
  - [ ] `governance-blind-spots.md`: Find gaps in hardening model
  - [ ] Each prompt is topology-blind (no reference to Known vectors or hardening source)

- [ ] **Behavioral Detectors Implemented:** `/agents/oth-red-team/detectors/`
  - [ ] Race condition detector (concurrent writes to same artifact)
  - [ ] Feedback loop detector (cyclic Issue creation)
  - [ ] Model-specific scanner (hardcoded refs to models/context windows)
  - [ ] Enumeration watcher (high rate of permission violations)
  - [ ] Supply chain analyzer (subtle semantic errors in data assumptions)
  - [ ] Each detector produces confidence score + evidence

- [ ] **Circuit-Breaker Automated:**
  - [ ] Level 1 (write rate) auto-enforces (pause agent for T minutes)
  - [ ] Level 2+ triggers OTH escalation (creates escalation Issue)
  - [ ] GitHub Actions workflow runs every 6 hours to check circuit-breaker status

- [ ] **First OTH Red-Team Cycle Executed:**
  - [ ] Krishna (or specialized red-team agent) runs OTH prompts against current merged artifacts
  - [ ] Behavioral detectors scan for OTH signatures
  - [ ] At least one OTH finding is identified (could be real or false positive)

- [ ] **OTH Promotion Workflow Tested:**
  - [ ] OTH escalation Issue is created (auto-populated template)
  - [ ] Human reviewer makes promotion decision (promote to Known / keep monitoring / false alarm)
  - [ ] If promoted: vector taxonomy is updated, hardening agent is updated, affected artifacts are re-evaluated
  - [ ] Promotion decision is documented with reasoning

- [ ] **OTH Dashboard Created:**
  - [ ] Shows: OTH candidates, escalation history, promotion decisions
  - [ ] Shows: circuit-breaker activations per agent
  - [ ] Shows: trend (OTH promotions per week, detector accuracy)

- [ ] **Krishna Sign-Off:**
  - [ ] Krishna sign-off: "OTH red-team cycle is complete; system is self-sustaining"

- [ ] **Ty Approval:**
  - [ ] Ty has reviewed OTH findings
  - [ ] Ty has reviewed promotion decision for at least one OTH
  - [ ] Ty sign-off: "OTH operations are live; GitYana is ready for Tier 1 use cases"

**Gate Status:** PASS or FAIL
- PASS → System is operational; ongoing OTH cadence begins (weekly red-team cycles)
- FAIL → Debug OTH detection / promotion workflow until working

---

## MASTER SIGN-OFF CHECKLIST

**For Ty to approve GitYana handoff to operations:**

- [ ] Sprint 1 deliverables locked (Vector taxonomy + Hardening agent + Circuit-breaker)
- [ ] Sprint 2 deliverables operational (Merge gates + first artifact merged)
- [ ] Sprint 3 deliverables operational (Permission model + Provenance + Audit)
- [ ] Sprint 4 deliverables operational (OTH red-team + promotion workflow)
- [ ] All Gates 1-6 PASS
- [ ] Yaki-ire and Krishna have signed off on their respective deliverables
- [ ] Documentation is complete (threat model, hardening guide, permission tiers, OTH playbook)
- [ ] First Tier 1 use case (e.g., autonomous PR review) is deployed and tested
- [ ] Escalation path is clear (who gets paged on circuit-breaker Level 4 trigger?)

**Ty Sign-Off Date:** ____________

---

**END OF DECISION GATES DOCUMENT**

Use this checklist to:
1. Document locked context before Sprint 0 starts
2. Validate deliverables at end of each sprint
3. Ensure no work begins until prerequisites are approved
4. Document ratification for audit trail
