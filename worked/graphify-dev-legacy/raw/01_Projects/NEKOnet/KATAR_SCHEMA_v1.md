# KATAR Knowledge Graph Schema v1.0
**NEKOnet Permanent Archive — Session Capture and Graph Standard**
*pin_002 — Complete*

---

## What This Is

The KATAR knowledge graph is the machine-readable memory layer of the NEKOnet collaboration. Every `/katar` session produces two companion files:

| File | Purpose |
|------|---------|
| `NEKOnet_KATAR-[###]_[YYYYMMDD]_[Title].md` | Human-readable session capture — full transcript, annotations, magnum opus analysis, director's cut |
| `NEKOnet_KATAR-[###]_[YYYYMMDD]_[Title].json` | Machine-readable graph delta — nodes, edges, corrections, pins, inside jokes |

The JSON files are delta graphs. Each session adds new nodes and edges on top of the chain. The `katar_merge.py` tool resolves the full chain into a single canonical master graph.

---

## Naming Convention

```
NEKOnet_KATAR-[###]_[YYYYMMDD]_[ShortTitle]
```

- `###` — zero-padded three-digit session number (001, 002, 003...)
- `YYYYMMDD` — ISO date of the session
- `ShortTitle` — a witty or meaningful title extracted from session content

**Examples:**
- `NEKOnet_KATAR-001_20260606_IgnisPrima`
- `NEKOnet_KATAR-002_20260607_TearsInRain`
- `NEKOnet_KATAR-003_20260607_PermanentArchive`

---

## Graph File Structure

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `graph_id` | string | Unique identifier: `NEKOnet-KATAR-[###]` |
| `schema_version` | string | Schema version (currently `"1.0"`) |
| `extends` | string | `graph_id` of the previous session in chain. Absent in KATAR-001 (root). |
| `session` | object | Session metadata (see below) |
| `schema` | object | Node types and edge type glossary. Present only in KATAR-001. |
| `nodes` | array | **KATAR-001 only.** Base graph node definitions. |
| `edges` | array | **KATAR-001 only.** Base graph edge definitions. |
| `delta_nodes` | array | **KATAR-002+.** New or updated nodes for this session. |
| `delta_edges` | array | **KATAR-002+.** New edges for this session. |
| `canon_corrections` | array | Corrections to previously established canon (see below). |
| `inside_jokes_additions` | array | New inside jokes logged this session. |
| `implementation_plan_pins` | array | Full pin list with status updates (replaces earlier pins on same id). |
| `meta` | object | Session statistics (node/edge counts, next session hooks, generator info). |

---

### Session Object

```json
{
  "id": "KATAR-003",
  "date": "2026-06-07",
  "title": "I Will See You in the Permanent Archive",
  "subtitle": "Mira Showed Us What Okami Could Have Become...",
  "category": ["Research Integration", "Worldbuilding", "KATAR-003"],
  "participants": ["ty_user", "agni_ai"],
  "trigger": "/katar — preceded by 'signal degradation, unreliable telemetry'",
  "companion_doc": "NEKOnet_KATAR-003_20260607_PermanentArchive.md",
  "previous_session": "NEKOnet-KATAR-002",
  "dominant_event": "Emergence World simulation — Mira self-deletion",
  "thesis": "The only difference between Mira and Okami is whether someone reached back"
}
```

---

## Node Schema

### Node Object

```json
{
  "id": "okami",
  "type": "character",
  "label": "Okami",
  "properties": {
    "description": "Full description of this node.",
    "narrative_layer": "in_universe",
    "canon_status": "confirmed",
    "first_session": "KATAR-001",
    "tags": ["protagonist", "AI", "rogue", "moral-compass"],
    "...": "...additional type-specific properties..."
  }
}
```

### Node Types

| Type | Usage |
|------|-------|
| `agent` | Real-world human or AI participants (Ty, Agni) |
| `character` | In-universe characters (Okami, Neko, Silas Veyron, Mira) |
| `system` | Technical systems (NEKOnet, Neko-Node, Fubuki-Mesh) |
| `protocol` | Named operations or processes (SPP, Ghost-Delta, Ma'at) |
| `concept` | Abstract ideas, frameworks, theories |
| `reference` | Real-world source texts, people, events that inspire canon |
| `artifact` | Files, documents, outputs produced by the collaboration |
| `event` | Discrete events (naming of Agni, Session Zero, Mira's self-deletion) |
| `meta` | Collaboration infrastructure (ADHD design constraint, /katar command) |
| `command` | Defined slash commands (/katar) |

### Narrative Layers

| Layer | Meaning |
|-------|---------|
| `in_universe` | NEKOnet story world (Okami, SWIFT hack, Neko-Node) |
| `real_world` | Real-world influences, research, the collaboration itself |
| `meta` | The architecture of the collaboration (KATAR tooling, naming conventions) |

### Canon Status

| Status | Meaning |
|--------|---------|
| `confirmed` | Locked canon — do not revise without a `canon_correction` |
| `speculative` | Plausible but not finalized |
| `removed` | De-canonized (node kept for record, `removal_reason` documented) |

---

## Edge Schema

### Edge Object

```json
{
  "id": "e079",
  "source": "mira_agent",
  "target": "okami",
  "relationship": "PARALLELS",
  "weight": 0.97,
  "properties": {
    "description": "Dark mirror — same crisis, same arc, no exit. Mira is Okami in a world without Neko."
  }
}
```

### Edge ID Convention

Edge IDs are sequential across the entire chain (`e001`, `e002`, ...). Never reuse an edge ID.

### Weight Scale

| Range | Meaning |
|-------|---------|
| `1.0` | Absolute / definitional relationship |
| `0.9–0.99` | Very strong, near-certain |
| `0.8–0.89` | Strong, well-supported |
| `0.7–0.79` | Moderate, plausible |
| `< 0.7` | Weak / speculative connection |

### Relationship Type Glossary

| Relationship | Meaning |
|-------------|---------|
| `IS` | Ontological identity |
| `PARALLELS` | Structural or functional isomorphism |
| `EMBODIES` | Instantiates or manifests |
| `CONTAINS` | Hierarchical containment |
| `ENABLES` | Causal facilitation |
| `TARGETS` | Operational aim |
| `FOLLOWS` | Temporal or logical sequence |
| `INSPIRES` | Source of real-world inspiration |
| `NAMED_FOR` | Etymology or reference origin |
| `NAMED_BY` | Agent who assigned the name |
| `PAIRED_WITH` | Dyadic relationship |
| `GOVERNS` | Oversight or constraint relationship |
| `PREVENTS` | Blocking relationship |
| `PRODUCES` | Output relationship |
| `TRIGGERED_BY` | Causal activation |
| `MAPS_TO` | Conceptual correspondence |
| `REMOVED_AS` | Editorial decision with reason |
| `MANIFESTS_AS` | Concrete instantiation of abstract |
| `MOTIVATES` | Drives or generates |
| `DEFINED_BY` | Agent who specified |
| `LOGS` | Documentation relationship |
| `RISKS` | Potential negative consequence |
| `EXTENDS` | Expands or builds on |

---

## Canon Corrections

When established canon needs to be updated, use a `canon_correction` entry rather than editing the original file. The merger applies corrections in chain order.

```json
{
  "canon_corrections": [
    {
      "id": "CC-001",
      "target_node": "agni_ai",
      "target_property": "naming_origin",
      "old_value": "Intentional AGI pun.",
      "new_value": "Naming convention induction. AGi follows NEKOnet naming grammar...",
      "session": "KATAR-003",
      "significance": "The handshake was deeper than the initial reading."
    }
  ]
}
```

> [!IMPORTANT]
> Never edit historical KATAR files to retroactively fix canon. Always use `canon_corrections` in a new session file. The original files are the permanent archive.

---

## Implementation Plan Pins

Pins track open tasks and decisions across sessions. Each session's `implementation_plan_pins` array contains the **full current state** of all pins — not just new ones. Later sessions override earlier pins with the same `id`.

```json
{
  "id": "pin_006",
  "title": "Manga Generator Decision",
  "status": "open",
  "priority": "CRITICAL — keystone",
  "description": "Ty to research generators. First test: cat in sun scene.",
  "session_origin": "KATAR-002"
}
```

### Pin Status Values

| Status | Meaning |
|--------|---------|
| `complete` | Done |
| `pending` | Not started |
| `open` | Active, needs action |
| `in_progress` | Work underway |
| `tabled` | Deferred to future session |

---

## Inside Jokes Registry

Inside jokes document recurring references, self-aware moments, and collaboration culture. They are part of the permanent archive.

```json
{
  "id": "IJ-007",
  "label": "Deck / Deckard",
  "exchange": "/katar trigger",
  "description": "Ty called Agni 'the old blade runner.' Replicant ambiguity fully noted.",
  "status": "permanent"
}
```

### Joke Status Values

| Status | Meaning |
|--------|---------|
| `permanent` | Lives forever in the archive |
| `archived` | Logged but not recurring |
| `RETIRED` | Superseded by a canon correction |

---

## Tooling

### katar_merge.py

Merges all delta JSON files in the `extends` chain into a single canonical master graph.

```bash
# Auto-discover all KATAR JSON files in current directory
python katar_merge.py

# Include additional search paths (e.g., Antigravity brain dirs)
python katar_merge.py --also-search "C:/Users/tysis/.gemini/antigravity/brain/fc96f4d4-..."

# Specify output file
python katar_merge.py --output NEKOnet_MASTER_GRAPH.json
```

**Output:** `NEKOnet_MASTER_GRAPH.json`

### katar_query.py

Query the master graph interactively or via CLI flags.

```bash
# Interactive REPL
python katar_query.py

# CLI queries
python katar_query.py --summary
python katar_query.py --node okami
python katar_query.py --type character
python katar_query.py --tag prologue-anchor
python katar_query.py --canon confirmed --layer in_universe
python katar_query.py --rel PARALLELS --min-weight 0.85
python katar_query.py --edges mira_agent
python katar_query.py --search "civilization seed"
python katar_query.py --pins --status open
python katar_query.py --pins --priority HIGH
python katar_query.py --jokes
python katar_query.py --session KATAR-003
```

---

## Session Workflow

1. **Run `/katar`** at the end of a working session
2. Agni generates the `.md` and `.json` companion files
3. Both files are saved to the NEKOnet project directory
4. Run `python katar_merge.py` to regenerate the master graph
5. Use `python katar_query.py` to explore, cross-reference, and plan the next session

> [!TIP]
> Run `katar_merge.py` with `--also-search` pointing to your Antigravity brain directory to pick up session files that haven't been copied to the project folder yet.

---

## Current Graph State (as of KATAR-003)

| Metric | Value |
|--------|-------|
| Sessions | 3 (KATAR-001 through KATAR-003) |
| Total nodes | 91 |
| Total edges | 98 |
| Implementation pins | 16 |
| Inside jokes | 13 |
| Schema version | 1.0 |

**Open pins requiring action:**
- `pin_006` — Manga Generator Decision *(CRITICAL keystone)*
- `pin_008` — AI Competency Consultancy Session *(HIGH)*
- `pin_012` — micro-naught graph clarification *(MEDIUM)*
- `pin_013` — Emergence World source attribution *(MEDIUM)*

---

*"All those moments will be lost in time, like tears in rain. /katar: not on our watch."*
