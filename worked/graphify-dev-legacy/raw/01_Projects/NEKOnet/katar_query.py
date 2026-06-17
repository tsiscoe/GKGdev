#!/usr/bin/env python3
"""
katar_query.py — NEKOnet Knowledge Graph Query Engine
======================================================
Query the NEKOnet master graph (NEKOnet_MASTER_GRAPH.json) by node type,
tag, canon_status, narrative_layer, session origin, relationship type,
weight thresholds, pin status, and full-text search.

Automatically runs katar_merge.py first if no master graph is found.

Usage examples:
    python katar_query.py --tag prologue-anchor
    python katar_query.py --type character
    python katar_query.py --canon confirmed --layer in_universe
    python katar_query.py --rel PARALLELS --min-weight 0.85
    python katar_query.py --node okami
    python katar_query.py --session KATAR-003
    python katar_query.py --search "civilization seed"
    python katar_query.py --pins --status open
    python katar_query.py --pins --priority HIGH
    python katar_query.py --summary
    python katar_query.py --jokes
    python katar_query.py  # interactive mode
"""

import json
import os
import sys
import argparse
import subprocess
import re
from pathlib import Path

# Force UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError)
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

DEFAULT_MASTER = "NEKOnet_MASTER_GRAPH.json"

ANSI = {
    "reset":   "\033[0m",
    "bold":    "\033[1m",
    "dim":     "\033[2m",
    "red":     "\033[91m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "cyan":    "\033[96m",
    "magenta": "\033[95m",
    "blue":    "\033[94m",
    "white":   "\033[97m",
}

# Disable ANSI on Windows if not supported
import platform
if platform.system() == "Windows":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        ANSI = {k: "" for k in ANSI}


def C(color: str, text: str) -> str:
    return f"{ANSI.get(color, '')}{text}{ANSI['reset']}"


def load_master(master_path: Path, auto_merge: bool = True) -> dict:
    """Load master graph, optionally triggering merge if not found."""
    if not master_path.exists():
        if auto_merge:
            print(C("yellow", f"\n  Master graph not found. Running katar_merge.py first...\n"))
            result = subprocess.run(
                [sys.executable, "katar_merge.py"],
                capture_output=False
            )
            if result.returncode != 0 or not master_path.exists():
                print(C("red", "\n  [ERROR] Merge failed. Run katar_merge.py manually first.\n"))
                sys.exit(1)
        else:
            print(C("red", f"\n  [ERROR] Master graph not found: {master_path}\n"))
            print("  Run: python katar_merge.py")
            sys.exit(1)

    with open(master_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_nodes(nodes: list, **criteria) -> list:
    """
    Filter nodes by any combination of:
        node_type, tag, canon_status, layer, session, search_text, node_id
    """
    results = []
    for node in nodes:
        props = node.get("properties", {})

        if criteria.get("node_id"):
            if node.get("id") != criteria["node_id"]:
                continue

        if criteria.get("node_type"):
            if node.get("type") != criteria["node_type"]:
                continue

        if criteria.get("canon_status"):
            if props.get("canon_status") != criteria["canon_status"]:
                continue

        if criteria.get("layer"):
            if props.get("narrative_layer") != criteria["layer"]:
                continue

        if criteria.get("session"):
            if props.get("first_session") != criteria["session"]:
                continue

        if criteria.get("tag"):
            tags = props.get("tags", [])
            if criteria["tag"] not in tags:
                continue

        if criteria.get("search_text"):
            term = criteria["search_text"].lower()
            blob = json.dumps(node).lower()
            if term not in blob:
                continue

        results.append(node)
    return results


def filter_edges(edges: list, **criteria) -> list:
    """
    Filter edges by:
        relationship, source, target, min_weight, max_weight, search_text
    """
    results = []
    for edge in edges:
        if criteria.get("relationship"):
            if edge.get("relationship") != criteria["relationship"].upper():
                continue

        if criteria.get("source"):
            if edge.get("source") != criteria["source"]:
                continue

        if criteria.get("target"):
            if edge.get("target") != criteria["target"]:
                continue

        weight = edge.get("weight", 0.0)
        if criteria.get("min_weight") is not None:
            if weight < criteria["min_weight"]:
                continue

        if criteria.get("max_weight") is not None:
            if weight > criteria["max_weight"]:
                continue

        if criteria.get("search_text"):
            term = criteria["search_text"].lower()
            blob = json.dumps(edge).lower()
            if term not in blob:
                continue

        results.append(edge)
    return results


def get_node_edges(graph: dict, node_id: str) -> tuple[list, list]:
    """Get all edges where node_id is source or target."""
    edges = graph.get("edges", [])
    outgoing = [e for e in edges if e.get("source") == node_id]
    incoming = [e for e in edges if e.get("target") == node_id]
    return outgoing, incoming


def filter_pins(pins: list, **criteria) -> list:
    """Filter implementation plan pins."""
    results = []
    for pin in pins:
        if criteria.get("status"):
            if pin.get("status", "").lower() != criteria["status"].lower():
                continue
        if criteria.get("priority"):
            pin_priority = pin.get("priority", "")
            if criteria["priority"].upper() not in pin_priority.upper():
                continue
        if criteria.get("session"):
            if pin.get("session_origin") != criteria["session"]:
                continue
        if criteria.get("search_text"):
            term = criteria["search_text"].lower()
            blob = json.dumps(pin).lower()
            if term not in blob:
                continue
        results.append(pin)
    return results


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_node(node: dict, verbose: bool = False):
    """Pretty-print a single node."""
    nid = node.get("id", "?")
    label = node.get("label", "?")
    ntype = node.get("type", "?")
    props = node.get("properties", {})

    canon = props.get("canon_status", "?")
    layer = props.get("narrative_layer", "?")
    session = props.get("first_session", "?")
    tags = props.get("tags", [])
    desc = props.get("description", "")

    # Color by canon status
    canon_colors = {
        "confirmed": "green",
        "speculative": "yellow",
        "removed": "red",
    }
    canon_color = canon_colors.get(canon, "white")

    print(f"\n  {C('bold', label)}  {C('dim', f'[{ntype}]')}  {C(canon_color, canon)}")
    print(f"  {C('dim', 'id:')} {nid}  {C('dim', 'layer:')} {layer}  {C('dim', 'session:')} {session}")
    if desc:
        # Wrap description at ~80 chars
        words = desc.split()
        line = "  "
        for word in words:
            if len(line) + len(word) > 82:
                print(C("dim", line))
                line = "  " + word + " "
            else:
                line += word + " "
        if line.strip():
            print(C("dim", line))
    if tags:
        print(f"  {C('cyan', 'tags:')} {' '.join(['#' + t for t in tags])}")

    if verbose:
        # Print all other properties
        skip = {"description", "tags", "canon_status", "narrative_layer", "first_session"}
        for k, v in props.items():
            if k in skip:
                continue
            v_str = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
            if len(v_str) > 120:
                v_str = v_str[:117] + "..."
            print(f"  {C('magenta', k + ':')} {v_str}")


def render_edge(edge: dict, node_label_map: dict = None):
    """Pretty-print a single edge."""
    src = edge.get("source", "?")
    tgt = edge.get("target", "?")
    rel = edge.get("relationship", "?")
    weight = edge.get("weight", 0.0)
    eid = edge.get("id", "?")
    desc = edge.get("properties", {}).get("description", "")

    src_label = node_label_map.get(src, src) if node_label_map else src
    tgt_label = node_label_map.get(tgt, tgt) if node_label_map else tgt

    weight_color = "green" if weight >= 0.9 else "yellow" if weight >= 0.7 else "red"

    print(f"\n  {C('cyan', src_label)} {C('bold', '─' + rel + '→')} {C('magenta', tgt_label)}")
    print(f"  {C('dim', f'[{eid}]')}  weight: {C(weight_color, str(weight))}")
    if desc:
        print(f"  {C('dim', desc)}")


def render_pin(pin: dict):
    """Pretty-print an implementation plan pin."""
    pid = pin.get("id", "?")
    title = pin.get("title", "?")
    status = pin.get("status", "?")
    priority = pin.get("priority", "")
    desc = pin.get("description", "")
    session = pin.get("session_origin", "")

    status_colors = {
        "complete": "green",
        "complete\n": "green",
        "pending": "yellow",
        "open": "cyan",
        "in_progress": "blue",
        "tabled": "dim",
    }
    scolor = status_colors.get(status.strip().lower(), "white")

    priority_color = "red" if "HIGH" in priority.upper() or "CRITICAL" in priority.upper() else "yellow"

    print(f"\n  {C('bold', pid + ':')} {title}")
    status_str = C(scolor, status)
    priority_str = C(priority_color, priority) if priority else ""
    session_str = C("dim", session) if session else ""
    meta_parts = [s for s in [status_str, priority_str, session_str] if s]
    print(f"  {' | '.join(meta_parts)}")
    if desc:
        print(f"  {C('dim', desc)}")


def render_joke(joke: dict):
    """Pretty-print an inside joke entry."""
    jid = joke.get("id", "?")
    label = joke.get("label", "?")
    exchange = joke.get("exchange", "?")
    desc = joke.get("description", "")
    status = joke.get("status", "?")

    status_color = "green" if status == "permanent" else "dim" if status == "archived" else "red"

    print(f"\n  {C('bold', jid + ':')} {label}  {C(status_color, '[' + status + ']')}")
    print(f"  {C('dim', 'exchange: ' + str(exchange))}")
    if desc:
        print(f"  {desc}")


def print_divider(title: str = ""):
    width = 60
    if title:
        pad = (width - len(title) - 2) // 2
        print(C("dim", "\n  " + "─" * pad + f" {title} " + "─" * pad))
    else:
        print(C("dim", "\n  " + "─" * width))


def print_count(label: str, count: int):
    color = "green" if count > 0 else "red"
    print(f"\n  {C('dim', label + ':')} {C(color, str(count))} result(s)")


# ---------------------------------------------------------------------------
# Summary view
# ---------------------------------------------------------------------------

def print_summary(graph: dict):
    """Print a high-level summary of the merged graph."""
    meta = graph.get("meta", {})
    chain = " → ".join(graph.get("session_chain", []))
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    # Count by type
    type_counts = {}
    canon_counts = {}
    layer_counts = {}
    for node in nodes:
        t = node.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
        c = node.get("properties", {}).get("canon_status", "unknown")
        canon_counts[c] = canon_counts.get(c, 0) + 1
        l = node.get("properties", {}).get("narrative_layer", "unknown")
        layer_counts[l] = layer_counts.get(l, 0) + 1

    # Count edges by relationship
    rel_counts = {}
    for edge in edges:
        r = edge.get("relationship", "unknown")
        rel_counts[r] = rel_counts.get(r, 0) + 1

    print_divider("NEKOnet Master Graph — Summary")
    print(f"\n  {C('bold', 'Generated:')} {graph.get('generated_at', '?')}")
    print(f"  {C('bold', 'Chain:')} {chain}")
    print(f"\n  {C('bold', 'Total nodes:')} {meta.get('total_nodes', len(nodes))}")
    print(f"  {C('bold', 'Total edges:')} {meta.get('total_edges', len(edges))}")

    print_divider("Nodes by Type")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {C('cyan', t):<30} {c}")

    print_divider("Nodes by Canon Status")
    canon_colors = {"confirmed": "green", "speculative": "yellow", "removed": "red"}
    for s, c in sorted(canon_counts.items(), key=lambda x: -x[1]):
        col = canon_colors.get(s, "white")
        print(f"  {C(col, s):<30} {c}")

    print_divider("Nodes by Layer")
    for l, c in sorted(layer_counts.items(), key=lambda x: -x[1]):
        print(f"  {C('magenta', l):<30} {c}")

    print_divider("Edges by Relationship")
    for r, c in sorted(rel_counts.items(), key=lambda x: -x[1]):
        print(f"  {C('blue', r):<30} {c}")

    print_divider()


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

INTERACTIVE_HELP = """
  ╔══════════════════════════════════════════════════════╗
  ║      KATAR Query Engine — Interactive Mode          ║
  ╠══════════════════════════════════════════════════════╣
  ║  Commands:                                          ║
  ║    summary                   Graph overview         ║
  ║    node <id>                 Get node by id         ║
  ║    type <type>               Nodes by type          ║
  ║    tag <tag>                 Nodes by tag           ║
  ║    canon <status>            Nodes by canon status  ║
  ║    layer <layer>             Nodes by layer         ║
  ║    session <KATAR-00N>       Nodes from session     ║
  ║    search <text>             Full-text search       ║
  ║    rel <RELATIONSHIP>        Edges by relationship  ║
  ║    edges <node_id>           All edges for a node   ║
  ║    weight <min>              Edges by min weight    ║
  ║    pins [status] [priority]  Implementation pins   ║
  ║    jokes                     Inside jokes registry  ║
  ║    types                     List all node types   ║
  ║    rels                      List all edge types   ║
  ║    tags                      List all tags          ║
  ║    help                      Show this help         ║
  ║    quit / exit / q           Exit                   ║
  ╚══════════════════════════════════════════════════════╝
"""


def get_node_label_map(graph: dict) -> dict:
    return {n["id"]: n.get("label", n["id"]) for n in graph.get("nodes", [])}


def interactive_mode(graph: dict):
    """Run an interactive query REPL."""
    print(INTERACTIVE_HELP)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    pins = graph.get("implementation_plan_pins", [])
    jokes = graph.get("inside_jokes", [])
    node_label_map = get_node_label_map(graph)

    while True:
        try:
            raw = input(C("cyan", "\n  katar> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print(C("dim", "\n\n  Exiting KATAR query engine.\n"))
            break

        if not raw:
            continue

        parts = raw.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("quit", "exit", "q"):
            print(C("dim", "\n  Exiting KATAR query engine.\n"))
            break

        elif cmd == "help":
            print(INTERACTIVE_HELP)

        elif cmd == "summary":
            print_summary(graph)

        elif cmd == "node":
            results = filter_nodes(nodes, node_id=arg)
            print_count("node", len(results))
            for n in results:
                render_node(n, verbose=True)
                out, inc = get_node_edges(graph, n["id"])
                if out or inc:
                    print_divider("Edges")
                    for e in out:
                        render_edge(e, node_label_map)
                    for e in inc:
                        render_edge(e, node_label_map)

        elif cmd == "type":
            results = filter_nodes(nodes, node_type=arg)
            print_count("type=" + arg, len(results))
            for n in results:
                render_node(n)

        elif cmd == "tag":
            results = filter_nodes(nodes, tag=arg)
            print_count("tag=" + arg, len(results))
            for n in results:
                render_node(n)

        elif cmd == "canon":
            results = filter_nodes(nodes, canon_status=arg)
            print_count("canon=" + arg, len(results))
            for n in results:
                render_node(n)

        elif cmd == "layer":
            results = filter_nodes(nodes, layer=arg)
            print_count("layer=" + arg, len(results))
            for n in results:
                render_node(n)

        elif cmd == "session":
            results = filter_nodes(nodes, session=arg)
            print_count("session=" + arg, len(results))
            for n in results:
                render_node(n)

        elif cmd == "search":
            n_results = filter_nodes(nodes, search_text=arg)
            e_results = filter_edges(edges, search_text=arg)
            print_count("nodes matching '" + arg + "'", len(n_results))
            for n in n_results:
                render_node(n)
            if e_results:
                print_count("edges matching '" + arg + "'", len(e_results))
                for e in e_results:
                    render_edge(e, node_label_map)

        elif cmd == "rel":
            results = filter_edges(edges, relationship=arg)
            print_count("rel=" + arg, len(results))
            for e in results:
                render_edge(e, node_label_map)

        elif cmd == "edges":
            out, inc = get_node_edges(graph, arg)
            node_label = node_label_map.get(arg, arg)
            print_divider(f"Outgoing from {node_label}")
            print_count("outgoing", len(out))
            for e in out:
                render_edge(e, node_label_map)
            print_divider(f"Incoming to {node_label}")
            print_count("incoming", len(inc))
            for e in inc:
                render_edge(e, node_label_map)

        elif cmd == "weight":
            try:
                min_w = float(arg)
                results = filter_edges(edges, min_weight=min_w)
                print_count(f"edges weight>={min_w}", len(results))
                for e in sorted(results, key=lambda x: -x.get("weight", 0)):
                    render_edge(e, node_label_map)
            except ValueError:
                print(C("red", "  [ERROR] weight requires a float, e.g.: weight 0.85"))

        elif cmd == "pins":
            # Parse optional status and priority from arg
            pin_args = arg.split() if arg else []
            status = None
            priority = None
            for pa in pin_args:
                if pa.lower() in ("complete", "pending", "open", "in_progress", "tabled"):
                    status = pa
                elif pa.upper() in ("HIGH", "MEDIUM", "LOW", "CRITICAL"):
                    priority = pa
            results = filter_pins(pins, status=status, priority=priority)
            print_count("pins", len(results))
            for p in results:
                render_pin(p)

        elif cmd == "jokes":
            print_count("inside jokes", len(jokes))
            for j in jokes:
                render_joke(j)

        elif cmd == "types":
            type_set = sorted(set(n.get("type", "?") for n in nodes))
            print(f"\n  {C('bold', 'Node types:')} {', '.join(C('cyan', t) for t in type_set)}")

        elif cmd == "rels":
            rel_set = sorted(set(e.get("relationship", "?") for e in edges))
            print(f"\n  {C('bold', 'Relationship types:')} {', '.join(C('blue', r) for r in rel_set)}")

        elif cmd == "tags":
            tag_set = set()
            for n in nodes:
                for t in n.get("properties", {}).get("tags", []):
                    tag_set.add(t)
            print(f"\n  {C('bold', 'All tags ({0}):'.format(len(tag_set)))}")
            for t in sorted(tag_set):
                print(f"    #{C('cyan', t)}")

        else:
            print(C("red", f"  [ERROR] Unknown command: '{cmd}'. Type 'help' for options."))


# ---------------------------------------------------------------------------
# CLI mode
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Query the NEKOnet merged knowledge graph.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--master", default=DEFAULT_MASTER, help="Path to master graph JSON.")
    parser.add_argument("--dir", default=".", help="Directory containing the master graph.")
    parser.add_argument("--no-merge", action="store_true", help="Don't auto-run merge if master not found.")

    # Node filters
    parser.add_argument("--node", help="Get node by exact id.")
    parser.add_argument("--type", dest="node_type", help="Filter nodes by type.")
    parser.add_argument("--tag", help="Filter nodes by tag.")
    parser.add_argument("--canon", dest="canon_status", help="Filter by canon_status.")
    parser.add_argument("--layer", help="Filter by narrative_layer.")
    parser.add_argument("--session", help="Filter by first_session (e.g., KATAR-003).")
    parser.add_argument("--search", help="Full-text search across nodes and edges.")

    # Edge filters
    parser.add_argument("--rel", help="Filter edges by relationship type.")
    parser.add_argument("--edges", dest="edges_for", help="Get all edges for a node id.")
    parser.add_argument("--min-weight", type=float, help="Filter edges by minimum weight.")

    # Pin filters
    parser.add_argument("--pins", action="store_true", help="Show implementation plan pins.")
    parser.add_argument("--status", help="Filter pins by status.")
    parser.add_argument("--priority", help="Filter pins by priority (HIGH, MEDIUM, LOW).")

    # Other views
    parser.add_argument("--jokes", action="store_true", help="Show inside jokes registry.")
    parser.add_argument("--summary", action="store_true", help="Show graph summary statistics.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show full node properties.")

    args = parser.parse_args()

    master_path = Path(args.dir) / args.master
    graph = load_master(master_path, auto_merge=not args.no_merge)
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    pins = graph.get("implementation_plan_pins", [])
    jokes = graph.get("inside_jokes", [])
    node_label_map = get_node_label_map(graph)

    # Determine if any filter args were given
    filter_args = [
        args.node, args.node_type, args.tag, args.canon_status, args.layer,
        args.session, args.search, args.rel, args.edges_for, args.min_weight,
        args.pins, args.jokes, args.summary
    ]
    any_filter = any(x is not None and x is not False for x in filter_args)

    if not any_filter:
        # No filters — launch interactive mode
        interactive_mode(graph)
        return

    if args.summary:
        print_summary(graph)

    if args.node:
        results = filter_nodes(nodes, node_id=args.node)
        print_count("node", len(results))
        for n in results:
            render_node(n, verbose=True)
            out, inc = get_node_edges(graph, n["id"])
            if out or inc:
                print_divider("Edges")
                for e in out + inc:
                    render_edge(e, node_label_map)

    if args.node_type or args.tag or args.canon_status or args.layer or args.session:
        results = filter_nodes(
            nodes,
            node_type=args.node_type,
            tag=args.tag,
            canon_status=args.canon_status,
            layer=args.layer,
            session=args.session,
        )
        label = " ".join(filter(None, [
            f"type={args.node_type}" if args.node_type else None,
            f"tag={args.tag}" if args.tag else None,
            f"canon={args.canon_status}" if args.canon_status else None,
            f"layer={args.layer}" if args.layer else None,
            f"session={args.session}" if args.session else None,
        ]))
        print_count(label, len(results))
        for n in results:
            render_node(n, verbose=args.verbose)

    if args.search:
        n_results = filter_nodes(nodes, search_text=args.search)
        e_results = filter_edges(edges, search_text=args.search)
        print_count(f"nodes matching '{args.search}'", len(n_results))
        for n in n_results:
            render_node(n)
        if e_results:
            print_count(f"edges matching '{args.search}'", len(e_results))
            for e in e_results:
                render_edge(e, node_label_map)

    if args.rel or args.min_weight is not None:
        results = filter_edges(
            edges,
            relationship=args.rel,
            min_weight=args.min_weight
        )
        label = " ".join(filter(None, [
            f"rel={args.rel}" if args.rel else None,
            f"weight>={args.min_weight}" if args.min_weight is not None else None,
        ]))
        print_count(label, len(results))
        for e in sorted(results, key=lambda x: -x.get("weight", 0)):
            render_edge(e, node_label_map)

    if args.edges_for:
        out, inc = get_node_edges(graph, args.edges_for)
        node_label = node_label_map.get(args.edges_for, args.edges_for)
        print_divider(f"Outgoing from {node_label}")
        for e in out:
            render_edge(e, node_label_map)
        print_divider(f"Incoming to {node_label}")
        for e in inc:
            render_edge(e, node_label_map)

    if args.pins:
        results = filter_pins(pins, status=args.status, priority=args.priority)
        print_count("pins", len(results))
        for p in results:
            render_pin(p)

    if args.jokes:
        print_count("inside jokes", len(jokes))
        for j in jokes:
            render_joke(j)

    print()


if __name__ == "__main__":
    main()
