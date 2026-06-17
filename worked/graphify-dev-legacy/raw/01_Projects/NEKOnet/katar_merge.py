#!/usr/bin/env python3
"""
katar_merge.py — NEKOnet Knowledge Graph Merger
================================================
Walks the KATAR `extends` chain, resolves all delta files in order,
applies canon_corrections, and produces a single merged canonical graph:
    NEKOnet_MASTER_GRAPH.json

Usage:
    python katar_merge.py                          # auto-discover all KATAR JSON files in CWD
    python katar_merge.py path/to/KATAR-001.json  # start from a specific root file
    python katar_merge.py --dir path/to/dir       # search a specific directory
    python katar_merge.py --output custom_name.json

The script resolves the chain by following `extends` fields, so file order
does not matter — it reconstructs the correct sequence automatically.
"""

import json
import os
import re
import sys
import argparse
import copy
from pathlib import Path
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def find_katar_files(search_dir: Path) -> list[Path]:
    """Find all KATAR JSON files in a directory."""
    pattern = re.compile(r"NEKOnet_KATAR-\d{3}[^.]*_.*\.json$", re.IGNORECASE)
    found = []
    for f in search_dir.iterdir():
        if f.is_file() and pattern.match(f.name) and not f.name.endswith(".metadata.json"):
            found.append(f)
    return found


def load_graph(path: Path) -> dict:
    """Load and parse a single KATAR JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data["_source_path"] = str(path)
        return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  [ERROR] Cannot load {path}: {e}")
        return None


def build_id_to_path(files: list[Path]) -> dict[str, Path]:
    """Map graph_id → file path for chain resolution."""
    mapping = {}
    for f in files:
        raw = load_graph(f)
        if raw and "graph_id" in raw:
            mapping[raw["graph_id"]] = f
    return mapping


# ---------------------------------------------------------------------------
# Chain resolution
# ---------------------------------------------------------------------------

def resolve_chain(files: list[Path], root_path: Path = None) -> list[dict]:
    """
    Resolve the extends chain and return graphs in correct order (oldest first).
    If root_path is given, start from that file.
    Otherwise, find the root (the file with no `extends`).
    """
    id_to_path = build_id_to_path(files)
    all_graphs = {gid: load_graph(p) for gid, p in id_to_path.items() if p is not None}

    # Root = the graph that has no `extends` field (it's the oldest in the chain)
    roots = [gid for gid, g in all_graphs.items() if "extends" not in g]

    if not roots:
        print("  [WARNING] Could not determine chain root — using alphabetical order.")
        return [g for g in all_graphs.values() if g]

    if root_path:
        # Override root with the user-specified file
        root_graph = load_graph(root_path)
        if root_graph:
            root_id = root_graph.get("graph_id")
        else:
            sys.exit(1)
    else:
        root_id = roots[0]
        if len(roots) > 1:
            print(f"  [WARNING] Multiple chain roots found: {roots}. Using: {root_id}")

    # Walk the chain forward
    chain = []
    current_id = root_id
    visited = set()

    while current_id and current_id not in visited:
        if current_id not in all_graphs:
            print(f"  [WARNING] Chain references '{current_id}' but no file found for it. Chain ends here.")
            break
        visited.add(current_id)
        graph = all_graphs[current_id]
        chain.append(graph)

        # Find the next in chain: a graph that extends current_id
        next_id = None
        for gid, g in all_graphs.items():
            if g.get("extends") == current_id:
                next_id = gid
                break
        current_id = next_id

    return chain


# ---------------------------------------------------------------------------
# Merge logic
# ---------------------------------------------------------------------------

def apply_canon_corrections(nodes: dict, corrections: list) -> dict:
    """Apply canon_corrections to the node map in place."""
    for correction in corrections:
        target_id = correction.get("target_node")
        target_prop = correction.get("target_property")
        new_value = correction.get("new_value")
        session = correction.get("session", "unknown")

        if target_id in nodes and target_prop:
            nodes[target_id]["properties"][target_prop] = new_value
            # Log the correction in the node
            if "_corrections_applied" not in nodes[target_id]["properties"]:
                nodes[target_id]["properties"]["_corrections_applied"] = []
            nodes[target_id]["properties"]["_corrections_applied"].append({
                "session": session,
                "property": target_prop,
                "new_value": new_value
            })
            print(f"  [CORRECTION] {target_id}.{target_prop} updated (from {session})")
        else:
            print(f"  [WARNING] Canon correction target not found: {target_id}")

    return nodes


def merge_graphs(chain: list[dict]) -> dict:
    """
    Merge a chain of graphs (oldest first) into a single canonical graph.

    Strategy:
    - KATAR-001 uses `nodes` and `edges` (base graph)
    - KATAR-002+ use `delta_nodes` and `delta_edges`
    - Later definitions override earlier ones (same node id = update)
    - canon_corrections are applied after all nodes are merged
    - All inside_jokes, implementation_plan_pins, and session metadata are collected
    """
    merged_nodes = {}   # id → node dict
    merged_edges = {}   # id → edge dict
    all_sessions = []
    all_inside_jokes = []
    all_pins = {}       # pin_id → pin dict (later overrides earlier)
    schema = {}
    canon_corrections_deferred = []  # apply after all nodes merged

    print(f"\n  Merging {len(chain)} graph(s) in chain order:")

    for graph in chain:
        session_id = graph.get("session", {}).get("id", "unknown")
        source = graph.get("_source_path", "unknown")
        print(f"    -> {session_id} ({Path(source).name})")

        # Schema (take from first graph that has it)
        if not schema and "schema" in graph:
            schema = graph["schema"]

        # Session metadata
        if "session" in graph:
            all_sessions.append(graph["session"])

        # Nodes — KATAR-001 uses `nodes`, deltas use `delta_nodes`
        node_list = graph.get("nodes", []) or graph.get("delta_nodes", [])
        for node in node_list:
            nid = node.get("id")
            if not nid:
                continue
            if nid in merged_nodes:
                # Merge properties (delta wins)
                existing_props = merged_nodes[nid].get("properties", {})
                new_props = node.get("properties", {})
                existing_props.update(new_props)
                merged_nodes[nid]["properties"] = existing_props
                merged_nodes[nid]["label"] = node.get("label", merged_nodes[nid].get("label"))
                merged_nodes[nid]["type"] = node.get("type", merged_nodes[nid].get("type"))
            else:
                merged_nodes[nid] = copy.deepcopy(node)

        # Edges — KATAR-001 uses `edges`, deltas use `delta_edges`
        edge_list = graph.get("edges", []) or graph.get("delta_edges", [])
        for edge in edge_list:
            eid = edge.get("id")
            if not eid:
                continue
            merged_edges[eid] = copy.deepcopy(edge)

        # Inside jokes
        jokes_list = graph.get("inside_jokes_additions", [])
        # Also check for inside_jokes_registry in KATAR-001
        if "inside_jokes_registry" in graph.get("nodes", [{}])[0] if graph.get("nodes") else False:
            pass  # Already captured via node merge
        for joke in jokes_list:
            all_inside_jokes.append(joke)

        # Implementation pins (later session overrides earlier for same id)
        pins_list = graph.get("implementation_plan_pins", [])
        for pin in pins_list:
            pid = pin.get("id")
            if pid:
                all_pins[pid] = copy.deepcopy(pin)

        # Collect canon corrections for deferred application
        corrections = graph.get("canon_corrections", [])
        canon_corrections_deferred.extend(corrections)

    # Apply canon corrections after all nodes are merged
    if canon_corrections_deferred:
        print(f"\n  Applying {len(canon_corrections_deferred)} canon correction(s):")
        merged_nodes = apply_canon_corrections(merged_nodes, canon_corrections_deferred)

    return {
        "graph_id": "NEKOnet-MASTER",
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generated_by": "katar_merge.py",
        "session_chain": [s.get("id") for s in all_sessions],
        "schema": schema,
        "nodes": list(merged_nodes.values()),
        "edges": list(merged_edges.values()),
        "inside_jokes": all_inside_jokes,
        "implementation_plan_pins": list(all_pins.values()),
        "sessions": all_sessions,
        "meta": {
            "total_nodes": len(merged_nodes),
            "total_edges": len(merged_edges),
            "total_sessions": len(all_sessions),
            "total_pins": len(all_pins),
            "total_inside_jokes": len(all_inside_jokes),
        }
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_master(master: dict, output_path: Path):
    """Write the merged master graph to disk."""
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(master, fh, indent=2, ensure_ascii=False)
    size_kb = output_path.stat().st_size / 1024
    print(f"\n  [OK] Master graph written -> {output_path.name} ({size_kb:.1f} KB)")


def print_summary(master: dict):
    """Print a brief merge summary."""
    m = master["meta"]
    chain = " -> ".join(master["session_chain"])
    print(f"""
  ---------------------------------------------
  NEKOnet Master Graph - Merge Summary
  ---------------------------------------------
  Session chain : {chain}
  Total nodes   : {m['total_nodes']}
  Total edges   : {m['total_edges']}
  Sessions      : {m['total_sessions']}
  Pins          : {m['total_pins']}
  Inside jokes  : {m['total_inside_jokes']}
  Generated at  : {master['generated_at']}
  ---------------------------------------------
""")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Merge KATAR knowledge graph delta files into a single canonical JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "root_file",
        nargs="?",
        help="Optional: path to the root (oldest) KATAR JSON file. If omitted, auto-discovered."
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="Directory to search for KATAR JSON files (default: current directory)."
    )
    parser.add_argument(
        "--output", "-o",
        default="NEKOnet_MASTER_GRAPH.json",
        help="Output filename (default: NEKOnet_MASTER_GRAPH.json)"
    )
    parser.add_argument(
        "--also-search",
        nargs="*",
        metavar="PATH",
        help="Additional directories or files to include in the search (e.g., Antigravity brain dirs)."
    )
    args = parser.parse_args()

    search_dir = Path(args.dir)
    output_path = search_dir / args.output

    print(f"\nKATAR Merge — NEKOnet Knowledge Graph Merger")
    print(f"  Searching: {search_dir.resolve()}")

    # Collect all KATAR files (deduplicated by filename stem)
    all_files = find_katar_files(search_dir)
    seen_stems = {f.stem for f in all_files}

    # Also search additional paths if provided
    if args.also_search:
        for extra in args.also_search:
            extra_path = Path(extra)
            if extra_path.is_dir():
                extra_files = find_katar_files(extra_path)
                new_files = [f for f in extra_files if f.stem not in seen_stems]
                all_files.extend(new_files)
                seen_stems.update(f.stem for f in new_files)
                print(f"  Also searching: {extra_path.resolve()} ({len(new_files)} new file(s) found)")
            elif extra_path.is_file():
                if extra_path.stem not in seen_stems:
                    all_files.append(extra_path)
                    seen_stems.add(extra_path.stem)
                    print(f"  Also including: {extra_path}")

    if not all_files:
        print("\n  [ERROR] No KATAR JSON files found. Check --dir path.")
        sys.exit(1)

    print(f"  Found {len(all_files)} KATAR file(s):")
    for f in all_files:
        print(f"    * {f.name}")

    # Resolve chain
    root_path = Path(args.root_file) if args.root_file else None
    chain = resolve_chain(all_files, root_path)

    if not chain:
        print("\n  [ERROR] Could not resolve graph chain.")
        sys.exit(1)

    # Merge
    master = merge_graphs(chain)

    # Write
    write_master(master, output_path)
    print_summary(master)

    print(f"  Run katar_query.py to explore the merged graph.\n")


if __name__ == "__main__":
    main()
