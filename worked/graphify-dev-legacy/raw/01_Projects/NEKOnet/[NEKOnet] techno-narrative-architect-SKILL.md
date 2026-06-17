---
name: techno-narrative-architect
description: Build technically-accurate dystopian narratives with branching storylines, multi-POV support, and automated tech validation. Designed for NEKO/net and similar universes with complex operational frameworks, distributed agent networks, and adversarial knowledge systems. Use this skill whenever the user is writing sci-fi, dystopian, or near-future fiction that involves complex plot branching (choose-your-own-adventure, multiple character POVs, timeline splits), needs to verify technical accuracy in narrative details (hacking, networks, AI, finance), or wants to visualize and explore how different story branches interconnect. This skill is essential for authors building coherent multi-branch narratives with authentic tech worldbuilding and CODEX-documented assets.
compatibility: Playwright, knowledge graph system (graphify or equivalent), Node.js, Python, NotebookLM integration (optional)
---

# Techno-Narrative Architect

A comprehensive system for authoring branching narratives with built-in technical accuracy validation and interactive visualization.

## Overview

This skill guides you through a three-layer workflow:

1. **Narrative authoring** — Structure your story as separate Markdown files with YAML metadata
2. **Knowledge graph construction** — Connect narrative branches to tech references and validate accuracy
3. **Interactive prototype generation** — Explore your story as a clickable HTML interface with branch visualization

The goal: build coherent, technically-authentic multi-branch narratives where you can test narrative integrity, track character arcs across timelines, and catch tech BS before it ships.

---

## Layer 1: Narrative Authoring

### Project Structure

Initialize your project with this structure:

```
project-name/
├── narrative/
│   ├── scenes/
│   │   ├── opening.md
│   │   ├── scene_001_branch_a.md
│   │   ├── scene_001_branch_b.md
│   │   └── ...
│   ├── arcs.md                    # Arc definitions (main + branches)
│   └── characters.md              # Character metadata
├── tech-references/
│   ├── built-in/                  # Provided tech DB
│   ├── custom/                    # Your project-specific tech rules
│   └── validation-rules.json       # Tech accuracy assertions
├── prototype/
│   ├── index.html
│   ├── graph.json                 # Narrative graph structure
│   └── decision-log.json           # Tracked paths
└── knowledge-graph/
    └── connections.json            # Narrative ↔ Tech linkages
```

### Scene File Format

Each scene is a separate Markdown file with YAML frontmatter. **Always** use this structure:

```markdown
---
id: scene_001_neon_arrival
title: Arrival in Neo-Kyoto
pov: [protagonist, antagonist]
timeline: main_2087
arc: opening_sequence
parent_branch: opening
branches:
  - branch_a:
      title: "Hack the checkpoint"
      condition: "protagonist has access_token"
      leads_to: scene_002_hack_route
      tech_required: [firewall_breach, ip_spoofing]
  - branch_b:
      title: "Bribe the guard"
      condition: "protagonist has credits >= 500"
      leads_to: scene_002_bribe_route
character_arcs:
  - protagonist: "learns_cost_of_compromise"
  - antagonist: "observes_protagonist_weakness"
subplot_tags: [political_conspiracy, romance_thread_a]
tech_elements: [firewall, SSH_protocol, zero_day_cve_2087_x]
integrity_check: "All branches reconverge at scene_010 for main plot"
---

# Neon Rain

The wet streets reflected... [narrative content in Markdown prose]

**Choice Point:**
- **Option A:** [description of branch_a]
- **Option B:** [description of branch_b]
```

### Key Metadata Fields

- **id** — Unique scene identifier (used by graph)
- **pov** — Array of character POVs in this scene
- **timeline** — Which timeline (e.g., `main_2087`, `branch_alternate_2087`)
- **arc** — Which story arc this belongs to
- **parent_branch** — What branch led here (for git-like structure)
- **branches** — Array of choices; each has `title`, `condition`, `leads_to`, and `tech_required`
- **tech_elements** — Array of tech references used in this scene (links to tech DB)
- **integrity_check** — Prose note about plot coherence at this node
- **character_arcs** — How character development progresses here

---

## Layer 2: Knowledge Graph & Tech Validation

### Tech Reference Database

Two sources of truth:

**1. Built-in database** (`tech-references/built-in/`) — real-world tech:
- CVEs and exploit chains (e.g., `CVE-2024-1234`, `supply_chain_attack`)
- Protocols and their constraints (SSH, SWIFT, BGP, DNS, etc.)
- Attack vectors with plausibility scores
- Real IP/domain/port conventions

**2. Custom rules** (`tech-references/custom/`) — project-specific:

```json
{
  "rule_id": "quantum_breaks_symmetric",
  "rule": "Operational quantum computers break symmetric crypto",
  "applies_to": ["AES-256", "ChaCha20"],
  "year_active": 2087,
  "reference": "Near-AGI timeline assumption"
}
```

### Knowledge Graph Connections

Run the knowledge graph connector (see scripts section) to link narrative scenes to tech references:

```json
{
  "scene_id": "scene_001_neon_arrival",
  "tech_connections": [
    {
      "element": "firewall_breach",
      "reference": "CVE-2087-firewall-bypass",
      "plausibility_score": 0.92,
      "validation_status": "accurate",
      "notes": "Multi-stage exploit chain documented in tech-db"
    },
    {
      "element": "ip_spoofing",
      "reference": "ip_spoofing_in_2087",
      "plausibility_score": 0.65,
      "validation_status": "warning",
      "notes": "Plausible but requires active network tap; most traffic is encrypted end-to-end"
    }
  ]
}
```

### Validation Rules

Define assertions in `validation-rules.json`:

```json
{
  "rules": [
    {
      "id": "no_impossible_ips",
      "type": "regex_reject",
      "pattern": "^(\\d{1,3}\\.){3}\\d{3,}|393\\.",
      "message": "IP address format is invalid. Valid IPs are 0-255.0-255.0-255.0-255",
      "severity": "critical"
    },
    {
      "id": "quantum_timeline_coherence",
      "type": "conditional",
      "rule": "If quantum_computers_operational == true AND year >= 2087, then all symmetric_crypto must be flagged as 'compromised'",
      "severity": "high"
    },
    {
      "id": "protocol_accuracy",
      "type": "reference_check",
      "check": "All mentioned protocols and CVEs exist in tech-references/",
      "severity": "high"
    }
  ]
}
```

---

## Layer 3: Interactive Prototype

### Graph Visualization

The prototype renders your narrative as an interactive graph:

- **Main timeline** — the primary story arc (trunk)
- **Branches** — alternate paths branching from decision points
- **Converges** — where branches rejoin the main line
- **Character arcs** — overlaid on nodes to show character development
- **Tech annotations** — warnings on nodes with tech accuracy issues

Nodes show:
- Scene title
- Decision point (if choice exists)
- Character POVs present
- Tech elements used (with validation status)

Edges show:
- Branch direction
- Condition for taking that branch
- Character presence across transitions

### Decision Tracking

As you explore, the prototype logs:

```json
{
  "session_id": "proto_explore_2024_05_23",
  "timestamp": "2024-05-23T14:32:00Z",
  "path_taken": [
    "opening",
    "scene_001 (chose branch_a: hack_checkpoint)",
    "scene_002_hack_route",
    "scene_010 (converged back to main)"
  ],
  "character_states": {
    "protagonist": ["learns_cost_of_compromise", "gains_system_access"],
    "antagonist": ["observes_weakness"]
  },
  "tech_stack_used": ["firewall_breach", "ip_spoofing", "ssh_exploit"],
  "plot_integrity_warnings": []
}
```

---

## Layer 4: CODEX Documentation

Paralleling your narrative authoring, generate **CODEX documents** for all world assets (characters, technology, locations, faction rules). These serve as the authoritative reference for your universe and integrate with your NotebookLM knowledge base.

### CODEX Structure

Each CODEX file follows this standardized format:

```
---
Document ID: NN-CODEX-[000]
Version: 1.0 (Main Canon)
Branch Origin: [Scene/Chat where concept originated]
Last Updated: [Date]
Status: [DRAFT / REVIEW / MERGED-CANON]
---

## 1. Executive Summary
[2-3 sentence elevator pitch of significance to NEKO/net]

## 2. Character Profile [If applicable]
- Designation/Alias, Faction, Role/Archetype
- Visual Design & Aesthetic (historical armor + cybernetic elements)
- Narrative & Motives

## 3. World Rules & Setting [If applicable]
- Location/Domain
- The System (How it works, unwritten rules)
- Historical/Cyber Friction (how tradition manifests in high-tech)
- Environmental Hazards & Aesthetics

## 4. Technology & Cybernetics [If applicable]
- Classification, Historical Counterpart
- Technical Specifications (Hardware, Software, Function)
- Limitations & Fail-Safes

## 5. Commit & Version History
[Table of versions, dates, authors, change log]
```

Keep placeholders intact across all CODEX files so your knowledge graph and NotebookLM can cross-reference accurately.

### CODEX Integration Workflow

```bash
python scripts/generate_codex.py \
  --scenes narrative/scenes/ \
  --characters narrative/characters.md \
  --output codex/ \
  --template codex-template.md
```

This creates CODEX entries for:
- Each character introduced in scenes
- Each technology/cyberware mentioned
- Each location/faction referenced
- World rules established

---

## Workflow: From Draft to Interactive Prototype

### Step 1: Write your scenes

Create `.md` files in `narrative/scenes/` using the format above. Start with the opening arc.

### Step 2: Initialize the knowledge graph

```bash
python scripts/init_knowledge_graph.py \
  --project-dir . \
  --tech-db tech-references/built-in/ \
  --custom-rules tech-references/custom/
```

This scans all `.md` files, extracts `tech_elements`, and builds a connection graph.

### Step 3: Validate technical accuracy

```bash
python scripts/validate_tech_accuracy.py \
  --scenes narrative/scenes/ \
  --rules tech-references/validation-rules.json \
  --output validation-report.json
```

Output flags:
- ✅ **Accurate** — tech is plausible and consistent with world rules
- ⚠️ **Warning** — plausible but requires justification
- ❌ **BS** — implausible, contradicts world rules or reality

Example output:
```json
{
  "scene": "scene_001_neon_arrival",
  "validations": [
    {
      "tech": "firewall_breach",
      "status": "accurate",
      "evidence": "CVE-2087-firewall-bypass documented in tech-db"
    },
    {
      "tech": "ip_spoofing",
      "status": "warning",
      "message": "In 2087 most traffic is encrypted end-to-end; spoofing alone won't work without active network tap"
    }
  ]
}
```

### Step 4: Generate the interactive prototype

```bash
python scripts/generate_prototype.py \
  --scenes narrative/scenes/ \
  --graph knowledge-graph/connections.json \
  --output prototype/index.html
```

Opens an interactive HTML prototype where you can:
- Click through story branches
- See the branch tree visualization
- Hover over tech elements to see validation status
- Track your path through the narrative

### Step 5: Iterate

Edit scenes, re-validate, regenerate. The prototype auto-updates.

---

## Analysis & Integrity Checks

### Plot Coherence Report

Generate a report showing:
- All branches and where they converge
- Character consistency across timelines
- Unresolved subplots
- Tech accuracy flags per scene

```bash
python scripts/plot_integrity_report.py \
  --scenes narrative/scenes/ \
  --output plot-report.md
```

Example output:
```markdown
# Plot Integrity Report

## Main Arc
- Opening → Scene 1 → Scene 2 → ... → Climax ✅

## Branch: Hack Route
- Scene 1 (chose hack) → Scene 2a → Scene 3a → Converges at Scene 10 ✅
- Character arcs: protagonist gains system access, antagonist detects intrusion
- Tech stack: [firewall_breach, SSH_exploit, privilege_escalation]
- Warnings: None

## Unresolved Subplots
- romance_thread_a: Last mentioned Scene 5, not resolved in any branch ⚠️

## Tech Accuracy
- 15 tech elements validated
- 14 accurate, 1 warning
- No critical BS detected ✅
```

### Character Arc Tracking

Verify characters develop consistently across all timelines:

```bash
python scripts/character_arc_analysis.py \
  --characters narrative/characters.md \
  --scenes narrative/scenes/ \
  --output character-analysis.json
```

Checks:
- Does each character appear in their expected POV scenes?
- Do character development tags form a coherent progression?
- Are character states consistent when branches reconverge?

---

## Bundled Resources

### Scripts

All scripts are in `scripts/`:
- `init_knowledge_graph.py` — Initialize knowledge graph from scenes
- `validate_tech_accuracy.py` — Run tech accuracy checks
- `generate_prototype.py` — Build interactive HTML prototype
- `plot_integrity_report.py` — Generate narrative coherence report
- `character_arc_analysis.py` — Track character development

### Tech Reference Database

`tech-references/built-in/`:
- `cves.json` — Real and plausible CVEs, mapped to year and platform
- `protocols.json` — Networking, crypto, and finance protocols with constraints
- `attack_vectors.json` — Exploit chains with plausibility scoring
- `worldbuilding.json` — Near-future assumptions (e.g., quantum crypto broken in 2087, SWIFT still operational)

### Validation Rules

`tech-references/validation-rules.json` — Pre-configured rules for common BS patterns:
- Impossible IPs
- Nonsense protocol names
- Progress bars for hacking
- Instant exploitation of "military-grade" systems
- Visible passwords
- Single points of failure in critical infrastructure
- Symmetric crypto broken by non-quantum computers

---

## Example: NEKO/net Opening Arc

To get started with **NEKO/net**, create this structure:

```
neko-net/
├── narrative/scenes/
│   ├── prologue_neon_rain.md          # Opening scene
│   ├── scene_001_checkpoint.md         # Checkpoint encounter (branch point)
│   ├── scene_002a_hack_route.md        # If protagonist hacks
│   ├── scene_002b_bribe_route.md       # If protagonist bribes
│   ├── scene_003_safe_house.md         # Converges
│   └── ...
├── tech-references/custom/
│   ├── neko_net_world_rules.json       # AGI, quantum ops, Pox Americana rules
│   ├── corporations.json               # Tech oligarchs and their capabilities
│   └── available_zero_days.json        # Exploits available in 2027
├── narrative/characters.md
└── narrative/arcs.md                   # Define main arc + branches
```

Start by writing `prologue_neon_rain.md`, then branch from there.

---

## Next Steps

1. **Initialize your project:** Run `init_knowledge_graph.py` on your narrative directory
2. **Write your opening arc:** Create 3-5 `.md` files for the opening, with at least one branch point
3. **Define tech references:** Add custom world rules to `validation-rules.json`
4. **Generate the prototype:** Run `generate_prototype.py` and explore your story interactively
5. **Iterate:** Edit scenes, re-validate, regenerate until plot and tech are solid

---

## Reference

- **Narrative format:** Markdown + YAML frontmatter (see above)
- **Tech accuracy:** Real CVEs, plausible attack chains, world-consistent rules
- **Visualization:** Interactive HTML graph with branch tracking and decision logging
- **Analysis:** Plot integrity, character arc coherence, tech validation reports
