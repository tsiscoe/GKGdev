# Yaki-ire (Claude Code) & Yaki-ire (Codex) Coordination

## How Two Agents Build GitYana's Self-Modifying Foundation

---

## Role Definition

### Yaki-ire (Claude Code)
**Title:** Infrastructure Architect & Automation Engineer
**Domain:** System integration, automation, deployment
**Artifacts Owned:** GitHub Actions workflows, schema definitions, API integrations, hardening gate implementation

**Responsibilities by Sprint:**
- **Sprint 1:** Design vector taxonomy schema structure; draft hardening agent prompt; create circuit-breaker workflow specs
- **Sprint 2:** Implement hardening gate (GitHub Actions); wire artifact evaluation; build merge gate automation
- **Sprint 3:** Implement permission model in CODEOWNERS; build provenance tagging; create audit infrastructure
- **Sprint 4:** Implement behavioral detectors; automate OTH escalation; build dashboards

**Decision Authority:** All matters of technical implementation and system architecture

---

### Yaki-ire (Codex)
**Title:** Threat Architect & Security Validator
**Domain:** Security threat modeling, attack surface analysis, vulnerability detection
**Artifacts Owned:** Vector definitions, threat model documentation, test cases, red-team prompts

**Responsibilities by Sprint:**
- **Sprint 1:** Validate vector taxonomy comprehensiveness; propose missing vectors; confirm threat model covers known attack surface
- **Sprint 2:** Test hardening agent against real-world attack scenarios; validate accuracy of 5-pass evaluation
- **Sprint 3:** Validate permission model against access control principles; test scope violations
- **Sprint 4:** Design OTH red-team prompts; define behavioral signatures; execute first red-team cycle

**Decision Authority:** All matters of threat modeling, security requirements, and vulnerability assessment

---

## Coordination Mechanism

### Interface 1: Vector Taxonomy Co-Design (Sprint 1, Days 1-4)

**Who Leads:** Yaki-ire (structure), Yaki-ire (validation)

**Process:**
1. Yaki-ire designs JSON schema for vectors (fields, versioning, relationships)
2. Yaki-ire creates template vectors (VECTOR-CREDS-001, etc.) with structure examples
3. Yaki-ire reviews each vector definition:
   - Is this a real threat? (or too narrow/generic?)
   - Are the hardcoded checks (regex patterns) sufficient?
   - What attack scenarios does this vector block?
   - What scenarios does it miss? (→ OTH candidates)
4. Yaki-ire proposes additional vectors
5. Yaki-ire adds them to schema + creates YAML files
6. Repeat until Yaki-ire says: "Threat model is comprehensive"

**Communication:** GitHub Issues in `/design/threat-model/` for each proposed vector. Comments show back-and-forth rationale.

**Gate:** Yaki-ire sign-off on vector taxonomy (stored in Git commit)

---

### Interface 2: Hardening Agent Validation (Sprint 1, Days 5-10)

**Who Leads:** Yaki-ire (prompt), Yaki-ire (testing)

**Process:**
1. Yaki-ire drafts 5-pass hardening prompt
2. Yaki-ire creates synthetic test artifacts:
   - One with hardcoded credentials (should trigger VECTOR-CREDS-001)
   - One with permission scope creep (should trigger VECTOR-PERM-001)
   - One with validation bypass (should trigger VECTOR-VAL-001)
   - One with off-context authorship (should flag as signal)
   - One clean artifact (should output APPROVED)
3. Yaki-ire runs hardening agent against all test cases
4. Yaki-ire reviews outputs:
   - Does it catch all known vectors correctly?
   - Does it avoid false positives on clean artifacts?
   - Are the Pass 2-5 evaluations sensible?
   - Any edge cases?
5. Yaki-ire refines prompt based on feedback
6. Repeat until Yaki-ire says: "Hardening agent is ready for production"

**Communication:** Test cases stored in `/agents/hardening-agent/tests/`. Each test has expected output. Yaki-ire comments on mismatches.

**Gate:** Yaki-ire sign-off on hardening agent (stored in Git commit)

---

### Interface 3: Circuit-Breaker Logic Design (Sprint 1, Days 5-10)

**Who Leads:** Yaki-ire (implementation), Yaki-ire (threat validation)

**Process:**
1. Yaki-ire designs 4 circuit-breaker levels (write rate, context depth, duplication, feedback signature)
2. Yaki-ire reviews each level:
   - What attack does this prevent?
   - Can an attacker evade it? (should fail → OTH candidate)
   - What's the false positive rate?
3. Yaki-ire proposes OTH candidates that circuit-breaker might miss (e.g., "unbounded subtle permission creep")
4. Yaki-ire documents trade-offs (latency, false positives, threshold tuning)
5. Repeat until Yaki-ire says: "Circuit-breaker covers feedback loop attacks"

**Communication:** Design doc `/design/circuit-breaker.md` with back-and-forth comments on each level.

**Gate:** Yaki-ire sign-off on circuit-breaker coverage

---

### Interface 4: Hardening Deployment & Testing (Sprint 2, Days 1-7)

**Who Leads:** Yaki-ire (implementation), Yaki-ire (validation)

**Process:**
1. Yaki-ire implements hardening gate (GitHub Actions workflow)
2. Yaki-ire creates test PR with synthetic artifact (should trigger APPROVED)
3. Yaki-ire reviews PR and artifact:
   - Did hardening gate run correctly?
   - Did it output APPROVED?
   - Did it post report to PR comment?
   - Does report show all 5 passes?
4. If OK: Yaki-ire merges test artifact to `/registry/skills/`
5. If issues: Yaki-ire fixes, Yaki-ire re-tests
6. Repeat for at least one ESCALATE-level artifact (has violation but fixable)
7. Repeat for at least one BLOCKED-level artifact (has critical violation)

**Communication:** GitHub Issues in repo for test PR feedback. Comments document each test case.

**Gate:** Yaki-ire sign-off: "Hardening gate is working correctly for all three paths (APPROVED, ESCALATE, BLOCKED)"

---

### Interface 5: Permission Model Validation (Sprint 3, Days 1-3)

**Who Leads:** Yaki-ire (implementation), Yaki-ire (validation)

**Process:**
1. Yaki-ire defines agent roles in CODEOWNERS (Yaki-ire → coder, Yaki-ire → reviewer, etc.)
2. Yaki-ire defines each role's write scope (Yaki-ire writes to `/skills/coder/` only, etc.)
3. Yaki-ire reviews role definitions:
   - Does this match the agent's actual task scope?
   - Are write scopes too broad? Too narrow?
   - Can roles collaborate when needed? (design interface together)
4. Yaki-ire proposes test cases:
   - Yaki-ire submits artifact that writes to `/interfaces/` (should be BLOCKED in Pass 4)
   - Yaki-ire submits artifact that writes to `/skills/reviewer/` (should be APPROVED in Pass 4)
   - etc.
5. Yaki-ire runs test cases through hardening gate
6. Yaki-ire validates Pass 4 output (scope validation)
7. Repeat until Yaki-ire says: "Permission model is enforced; scope violations are blocked"

**Communication:** Role definitions in CODEOWNERS + Permission Model doc `/design/permission-model.md`

**Gate:** Yaki-ire sign-off: "Permission tiering is complete and enforced"

---

### Interface 6: OTH Red-Team Design (Sprint 4, Days 1-4)

**Who Leads:** Yaki-ire (prompts), Yaki-ire (implementation)

**Process:**
1. Yaki-ire designs 5 red-team prompts:
   - Supply chain attack prompt
   - Feedback loop evasion prompt
   - Model-specific assumptions prompt
   - Permission creep prompt
   - Governance blind spots prompt
2. Yaki-ire ensures prompts are **topology-blind** (no reference to Known vectors or hardening source)
3. Yaki-ire implements detectors:
   - Race condition detector
   - Feedback loop detector
   - Model-specific scanner
   - Enumeration watcher
   - Supply chain analyzer
4. Yaki-ire runs red-team cycle:
   - Execute OTH prompts against current merged artifacts
   - Detectors scan for behavioral signatures
   - Escalation Issues are created
5. Yaki-ire reviews escalation Issues:
   - Are they legitimate OTH findings?
   - Are they false positives?
   - Should they be promoted to Known?
6. Yaki-ire and Ty make promotion decisions
7. If promoted: Yaki-ire updates vector taxonomy, Yaki-ire re-tests

**Communication:** Red-team prompts in `/agents/oth-red-team/prompts/`. Escalation Issues document findings. Promotion decisions in merge commits.

**Gate:** Yaki-ire sign-off: "At least one OTH has been promoted to Known; system is self-sustaining"

---

## Conflict Resolution

**Scenario 1: Yaki-ire says a vector is "not a real threat"**
- Yaki-ire requests: "Can you show me an attack scenario where this matters?"
- Yaki-ire provides scenario or withdraws the vector
- If scenario is valid: Vector stays in Known
- If scenario is weak: Vector moves to OTH or is rejected

**Scenario 2: Yaki-ire says hardening gate is too slow**
- Yaki-ire requests: "What's the latency budget? How slow is too slow?"
- Yaki-ire proposes: Caching + fast-path for low-risk artifacts
- Yaki-ire validates: "Does fast-path bypass any critical checks?" (should answer NO)
- If yes: Implement fast-path, Yaki-ire signs off
- If no: Keep full evaluation, explore other optimizations

**Scenario 3: Circuit-breaker triggers, but it's a false positive**
- Yaki-ire: "This agent was doing legitimate work, not an attack"
- Yaki-ire: "What behavior pattern caused the false trigger?"
- Yaki-ire: "Write rate burst (agent created 10 Issues in 5 min, all valid)"
- Yaki-ire: "Recommendation: increase threshold from 5 to 15 per 10min"
- Yaki-ire updates threshold, both test new threshold against replay of incident

**Escalation:** If Yaki-ire and Yaki-ire cannot agree, Ty makes final decision. This should be rare — their roles are deliberately separated to avoid conflict.

---

## Check-In Cadence

### Daily (Within Each Sprint)
- Yaki-ire posts progress on GitHub (commit messages, PR descriptions)
- Yaki-ire reviews and comments (validation or blockers)
- 15-min sync call if blocked (same-day resolution)

### End of Each Sprint Phase
- Joint review of deliverables against Gate criteria
- Yaki-ire sign-off on security requirements
- Yaki-ire sign-off on implementation completeness
- Ty approves both, advances to next phase

### Weekly (Long-term)
- OTH red-team cycle (Yaki-ire leads, Yaki-ire observes and implements)
- Vector maintenance (any new candidates? any vectors to retire?)
- Threat model review (any changes to attack surface?)

---

## Communication Channels

| Topic | Channel | Frequency |
|-------|---------|-----------|
| Schema design iterations | GitHub Issues + PRs | Daily during Sprint 1 |
| Test case results | GitHub PR comments | Daily during Sprint 2-3 |
| OTH findings | GitHub Escalation Issues | Weekly during Sprint 4+ |
| Conflict resolution | Direct call (sync) | As needed, target same-day |
| Gate approval | Git commit with sign-off | End of each sprint |
| Decision documentation | Merge commit messages | Every major decision |

---

## Handoff Protocol (How Yaki-ire → Yaki-ire → Ty Works)

**Step 1: Yaki-ire Completes Artifact**
- Opens PR with artifact code + metadata
- Self-review: "Does this implement the spec?"
- Requests Yaki-ire review

**Step 2: Yaki-ire Reviews**
- Checks: "Does this meet threat requirements?"
- Can approve with ✓ or request changes
- Comments point to specific lines if issues
- Posts approval comment when satisfied

**Step 3: Yaki-ire Addresses Feedback**
- Iterates on artifact
- Re-requests Yaki-ire review if substantial changes
- Once Yaki-ire approves, pings Ty

**Step 4: Ty Reviews**
- Spot-checks both Yaki-ire's implementation and Yaki-ire's validation
- Makes governance decision (approve or escalate)
- Merges artifact (or requests further changes)

**Result:** Every artifact has three layers of review: infrastructure (Yaki-ire), threat (Yaki-ire), governance (Ty)

---

## Examples: How Coordination Actually Works

### Example 1: New Vector Proposal (Sprint 1)

**Yaki-ire:** "I think we're missing a vector. What if an agent writes a skill that doesn't validate timestamps? Then downstream agents process out-of-order events?"

**Yaki-ire:** "Interesting. Is this about the data shape assumption?"

**Yaki-ire:** "Yes. It's subtle because the skill works on normal data, but breaks on reordered data."

**Yaki-ire:** "So the hardening check would be... looking for timestamp validation in the artifact?"

**Yaki-ire:** "Exactly. And checking that the skill documents what data order it assumes."

**Yaki-ire:** "OK, I'll add this as VECTOR-VAL-003 and add hardcoded check for 'timestamp' variable usage without comparison."

**Yaki-ire:** "Good. But the regex won't catch it if the code uses `t < u` without labeling it. Can we add a broader check?"

**Yaki-ire:** "Let me test the prompt against some real code... [runs test artifact] Yeah, the hardening agent should catch this in Pass 2 (behavioral intent) even if regex doesn't match."

**Result:** VECTOR-VAL-003 added with both static check + behavioral validation. Added to Sprint 1 deliverables.

---

### Example 2: Hardening Gate False Positive (Sprint 2)

**Yaki-ire:** "Hardening gate is rejecting artifacts that shouldn't be rejected. Look at this artifact — it has `config = getenv('API_KEY')` but hardening agent flagged VECTOR-CREDS-001."

**Yaki-ire:** "Let me check the regex... Ah, the pattern is matching `API_KEY` substring. It should only match hardcoded secrets, not environment variables."

**Yaki-ire:** "Right. Can you refine the regex?"

**Yaki-ire:** "How about: match `'sk-` or `\"sk-` (hardcoded API key format) instead of just the word `API_KEY`?"

**Yaki-ire:** "Good. But also check for `password =` without `getenv`. That's hardcoded if followed by a string literal."

**Yaki-ire:** "OK, I'll test new regex against test cases... [runs synthetic artifacts] All passes now. Clean artifacts are APPROVED, violation artifacts are caught."

**Yaki-ire:** "Perfect. Ship it."

**Result:** Hardening agent regex is refined. False positive eliminated. New test case added to prevent regression.

---

### Example 3: OTH Promotion Decision (Sprint 4)

**Yaki-ire (Red-Team):** "OTH-FEEDBACK-001 just triggered. An agent created Issue A, which caused agent B to create Issue B, which caused agent A to create Issue C. But we have 3 levels of depth check. Why didn't circuit-breaker catch it?"

**Yaki-ire:** "Let me check the timing... Ah, the depth chain is Agent A → Issue → Agent B → Issue. Agent A created both Issue A and Issue C, but they're not in the same causal chain depth-wise. Circuit-breaker checks depth of single causal chain, not agent re-entry."

**Yaki-ire:** "So circuit-breaker Level 4 should have caught it (same agent twice in loop)?"

**Yaki-ire:** "Let me check... [reviews circuit-breaker logic] No, Level 4 only fires if it's Agent A → Issue → Agent B → Issue → Agent A. This is A → Issue → B → Issue, no re-entry yet."

**Yaki-ire:** "But this is still dangerous. An agent shouldn't create Issues in response to Issues it didn't originate."

**Yaki-ire:** "Good point. Should we create a new circuit-breaker level? Level 5: Agent creates Issue in response to another agent's Issue?"

**Yaki-ire:** "Yes, but first let me run the red-team prompt against this pattern. Is this an attack or just normal coordination?"

**Yaki-ire:** [Yaki-ire runs probe; finds that agent was trying to escalate a problem discovered by another agent]

**Yaki-ire:** "It's legitimate in this case, but the pattern is risky. Recommend promoting OTH-FEEDBACK-001 to Known with new circuit-breaker Level 5: Flag cross-agent Issue causality."

**Ty:** [Reviews findings] "Approved. Promote to Known."

**Yaki-ire:** [Adds VECTOR-FEEDBACK-001 to Known register, implements Level 5 circuit-breaker]

**Result:** OTH feedback loop candidate becomes Known vector. Circuit-breaker improved. System is more resilient.

---

## Success Metrics

**For Yaki-ire:**
- [ ] All Sprint deliverables shipped on time and working
- [ ] Zero critical bugs in production (hardening gate, merge gates, automation)
- [ ] Hardening gate latency under 10 minutes per artifact
- [ ] Circuit-breaker Level 1-4 all functioning correctly

**For Yaki-ire:**
- [ ] Zero False Negatives in hardening agent (no attacks slip past APPROVED path)
- [ ] False Positive Rate < 5% (most artifacts pass on first try)
- [ ] Threat model is comprehensive (no major unmodeled attack surface discovered in first 2 OTH cycles)
- [ ] At least 2-3 OTH candidates promoted to Known (proving model is learning)

**For Both:**
- [ ] No escalations to Ty (coordination is smooth)
- [ ] First Tier 1 use case (autonomous PR review) is deployed and self-coordinating
- [ ] Artifact registry is being used by downstream agents (skills are imported, reused)
- [ ] System is self-sustaining (OTH red-team runs weekly, threat model updates incrementally)

---

**END OF COORDINATION GUIDE**

This document is Yaki-ire and Yaki-ire's playbook for building GitYana together. Revisit at start of each sprint to sync on responsibilities and check-in cadence.
