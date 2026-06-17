"""
katar_visualize.py — NEKOnet Master Graph Visualizer
Reads NEKOnet_MASTER_GRAPH.json and outputs an interactive HTML graph via pyvis.
"""

import sys
import json
import argparse
import webbrowser
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    from pyvis.network import Network
except ImportError:
    print("  pyvis not installed. Run: pip install pyvis")
    sys.exit(1)

# ── Color palette by node type ──────────────────────────────────────────────
NODE_COLORS = {
    "character":  {"bg": "#E8854A", "border": "#C4622A", "font": "#1a1a1a"},
    "concept":    {"bg": "#4A7FE8", "border": "#2A5CC4", "font": "#ffffff"},
    "system":     {"bg": "#2ABFBF", "border": "#1A8F8F", "font": "#1a1a1a"},
    "protocol":   {"bg": "#9B59B6", "border": "#7D3C98", "font": "#ffffff"},
    "artifact":   {"bg": "#F0C040", "border": "#C49A20", "font": "#1a1a1a"},
    "event":      {"bg": "#E84A6A", "border": "#C42A4A", "font": "#ffffff"},
    "meta":       {"bg": "#7F8C8D", "border": "#5D6D6E", "font": "#ffffff"},
    "agent":      {"bg": "#27AE60", "border": "#1E8449", "font": "#ffffff"},
    "reference":  {"bg": "#85C1E9", "border": "#5499C7", "font": "#1a1a1a"},
    "command":    {"bg": "#C0392B", "border": "#922B21", "font": "#ffffff"},
}
DEFAULT_COLOR = {"bg": "#BDC3C7", "border": "#95A5A6", "font": "#1a1a1a"}

# ── Edge colors by relationship ──────────────────────────────────────────────
EDGE_COLORS = {
    "PARALLELS":     "#4A7FE8",
    "ENABLES":       "#27AE60",
    "PRODUCES":      "#F39C12",
    "MAPS_TO":       "#9B59B6",
    "CONTAINS":      "#7F8C8D",
    "INSPIRES":      "#E84A6A",
    "NAMED_FOR":     "#E8854A",
    "EMBODIES":      "#2ABFBF",
    "PAIRED_WITH":   "#F0C040",
    "IS":            "#BDC3C7",
    "RISKS":         "#C0392B",
    "PREVENTS":      "#27AE60",
    "MANIFESTS_AS":  "#9B59B6",
    "MOTIVATES":     "#E8854A",
    "CREATED":       "#F39C12",
    "NAMED_BY":      "#E8854A",
    "DEFINED_BY":    "#4A7FE8",
    "REMOVED_AS":    "#C0392B",
    "FOLLOWS":       "#7F8C8D",
    "GOVERNS":       "#9B59B6",
    "TRIGGERED_BY":  "#E84A6A",
    "EXTENDS":       "#4A7FE8",
    "DEFINES":       "#2ABFBF",
    "WORKED_ON":     "#27AE60",
}
DEFAULT_EDGE_COLOR = "#95A5A6"

# ── Layer shapes ─────────────────────────────────────────────────────────────
LAYER_SHAPES = {
    "in_universe": "dot",
    "real_world":  "square",
    "meta":        "diamond",
}

REMOVED_STYLE = {"bg": "#3D3D3D", "border": "#1a1a1a", "font": "#888888"}


def build_tooltip(node: dict) -> str:
    p = node.get("properties", {})
    lines = [f"<b>{node.get('label', node['id'])}</b>",
             f"<i>type: {node.get('type','?')} | layer: {p.get('narrative_layer','?')} | canon: {p.get('canon_status','?')}</i>",
             ""]
    desc = p.get("description", "")
    if desc:
        lines.append(desc[:400] + ("…" if len(desc) > 400 else ""))
    tags = p.get("tags", [])
    if tags:
        lines.append("")
        lines.append("Tags: " + " ".join(f"#{t}" for t in tags[:8]))
    return "<br>".join(lines)


def build_edge_tooltip(edge: dict) -> str:
    p = edge.get("properties", {})
    desc = p.get("description", "")
    return f"<b>{edge['relationship']}</b> (weight {edge.get('weight',0):.2f})<br>{desc[:300]}"


def main():
    parser = argparse.ArgumentParser(description="NEKOnet Master Graph Visualizer")
    parser.add_argument("--graph",   default="NEKOnet_MASTER_GRAPH.json", help="Path to master graph JSON")
    parser.add_argument("--output",  default="NEKOnet_GRAPH_VIZ.html",    help="Output HTML file")
    parser.add_argument("--layer",   default=None, help="Filter by layer: in_universe | real_world | meta")
    parser.add_argument("--type",    default=None, help="Filter by node type: character | concept | system …")
    parser.add_argument("--no-open", action="store_true", help="Don't auto-open in browser")
    parser.add_argument("--physics", action="store_true", help="Keep physics enabled (slower but dynamic)")
    args = parser.parse_args()

    graph_path = Path(args.graph)
    if not graph_path.exists():
        print(f"  [ERROR] Graph file not found: {graph_path}")
        sys.exit(1)

    print(f"\n  NEKOnet Graph Visualizer")
    print(f"  Reading: {graph_path}")

    with open(graph_path, encoding="utf-8") as f:
        graph = json.load(f)

    nodes_raw = graph.get("nodes", [])
    edges_raw = graph.get("edges", [])

    # ── Apply filters ────────────────────────────────────────────────────────
    if args.layer:
        nodes_raw = [n for n in nodes_raw
                     if n.get("properties", {}).get("narrative_layer") == args.layer]
        print(f"  Filter: layer={args.layer}")
    if args.type:
        nodes_raw = [n for n in nodes_raw if n.get("type") == args.type]
        print(f"  Filter: type={args.type}")

    visible_ids = {n["id"] for n in nodes_raw}
    edges_raw = [e for e in edges_raw
                 if e["source"] in visible_ids and e["target"] in visible_ids]

    print(f"  Nodes: {len(nodes_raw)}  |  Edges: {len(edges_raw)}")

    # ── Compute degree for node sizing ───────────────────────────────────────
    degree = {n["id"]: 0 for n in nodes_raw}
    for e in edges_raw:
        degree[e["source"]] = degree.get(e["source"], 0) + 1
        degree[e["target"]] = degree.get(e["target"], 0) + 1

    # ── Build pyvis network ──────────────────────────────────────────────────
    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#0D1117",
        font_color="#E6EDF3",
        directed=True,
        notebook=False,
    )

    net.set_options("""
    {
      "nodes": {
        "font": { "size": 13, "face": "Inter, Segoe UI, sans-serif" },
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "shadow": { "enabled": true, "size": 8, "x": 2, "y": 2 }
      },
      "edges": {
        "arrows": { "to": { "enabled": true, "scaleFactor": 0.6 } },
        "smooth": { "type": "curvedCW", "roundness": 0.2 },
        "font": { "size": 10, "face": "Inter, Segoe UI, sans-serif", "align": "middle" },
        "shadow": { "enabled": false }
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.3,
          "springLength": 180,
          "springConstant": 0.04,
          "damping": 0.15
        },
        "stabilization": { "iterations": 200, "fit": true }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "hideEdgesOnDrag": true,
        "multiselect": true,
        "navigationButtons": true
      }
    }
    """)

    # ── Add nodes ────────────────────────────────────────────────────────────
    for node in nodes_raw:
        nid    = node["id"]
        ntype  = node.get("type", "concept")
        props  = node.get("properties", {})
        layer  = props.get("narrative_layer", "meta")
        status = props.get("canon_status", "unknown")

        color_def = NODE_COLORS.get(ntype, DEFAULT_COLOR)
        if status == "removed":
            color_def = REMOVED_STYLE
        elif status == "speculative":
            color_def = {**color_def, "border": "#F39C12"}

        shape = LAYER_SHAPES.get(layer, "dot")
        size  = 14 + min(degree.get(nid, 0) * 3, 30)
        label = node.get("label", nid)
        # Truncate long labels for display
        display_label = label if len(label) <= 28 else label[:26] + "…"

        net.add_node(
            nid,
            label=display_label,
            title=build_tooltip(node),
            color={"background": color_def["bg"],
                   "border":     color_def["border"],
                   "highlight":  {"background": "#FFFFFF", "border": color_def["border"]},
                   "hover":      {"background": "#F8F9FA", "border": color_def["border"]}},
            font={"color": color_def["font"], "size": 13},
            shape=shape,
            size=size,
            mass=max(1, degree.get(nid, 0) * 0.5),
        )

    # ── Add edges ────────────────────────────────────────────────────────────
    for edge in edges_raw:
        rel    = edge.get("relationship", "RELATES")
        weight = edge.get("weight", 0.5)
        color  = EDGE_COLORS.get(rel, DEFAULT_EDGE_COLOR)

        net.add_edge(
            edge["source"],
            edge["target"],
            title=build_edge_tooltip(edge),
            label=rel,
            color={"color": color, "opacity": 0.6 + weight * 0.4,
                   "highlight": "#FFFFFF", "hover": "#FFFFFF"},
            width=0.5 + weight * 2.5,
            dashes=(weight < 0.7),
        )

    # ── Legend HTML injection ────────────────────────────────────────────────
    legend_html = """
<style>
  body { font-family: 'Inter', 'Segoe UI', sans-serif; }
  #legend {
    position: fixed; top: 16px; right: 16px; z-index: 9999;
    background: rgba(13,17,23,0.92); border: 1px solid #30363D;
    border-radius: 10px; padding: 14px 18px; color: #E6EDF3;
    font-size: 12px; min-width: 180px; backdrop-filter: blur(8px);
  }
  #legend h3 { margin: 0 0 10px; font-size: 13px; color: #58A6FF; }
  .leg-row { display: flex; align-items: center; gap: 8px; margin: 5px 0; }
  .leg-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
  .leg-sq  { width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; }
  #stats { margin-top: 12px; padding-top: 10px; border-top: 1px solid #30363D;
           color: #8B949E; font-size: 11px; }
  #controls { margin-top: 10px; padding-top: 10px; border-top: 1px solid #30363D; }
  #controls button {
    background: #21262D; border: 1px solid #30363D; color: #E6EDF3;
    padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 11px;
    margin: 2px 0; width: 100%;
  }
  #controls button:hover { background: #30363D; }
</style>
<div id="legend">
  <h3>◈ NEKOnet Graph</h3>
""" + "".join([
    f'  <div class="leg-row"><div class="leg-dot" style="background:{v["bg"]};border:2px solid {v["border"]}"></div><span>{k}</span></div>\n'
    for k, v in NODE_COLORS.items()
]) + """
  <div style="margin-top:8px;font-size:11px;color:#8B949E">
    Shape: ● in-universe &nbsp;■ real_world &nbsp;◆ meta
  </div>
  <div style="margin-top:4px;font-size:11px;color:#8B949E">
    Dashed edge = weight &lt; 0.7
  </div>
""" + f"""
  <div id="stats">
    Nodes: {len(nodes_raw)} &nbsp;|&nbsp; Edges: {len(edges_raw)}<br>
    Sessions: KATAR-001 → 005
  </div>
  <div id="controls">
    <button onclick="network.fit()">⊞ Fit all</button>
    <button onclick="network.setOptions({{physics:{{enabled:true}}}});setTimeout(()=>network.setOptions({{physics:{{enabled:false}}}}),3000)">↺ Re-layout</button>
  </div>
</div>
"""

    # ── Write output ─────────────────────────────────────────────────────────
    output_path = Path(args.output)
    net.save_graph(str(output_path))

    # Inject legend into the HTML
    html = output_path.read_text(encoding="utf-8")
    html = html.replace("</body>", legend_html + "\n</body>")
    output_path.write_text(html, encoding="utf-8")

    print(f"\n  ─────────────────────────────────────────")
    print(f"  Graph written → {output_path}")
    print(f"  ─────────────────────────────────────────")
    print(f"  Nodes: {len(nodes_raw)}  |  Edges: {len(edges_raw)}")
    print(f"  Filters: layer={args.layer or 'all'}  type={args.type or 'all'}")
    print(f"\n  Controls:")
    print(f"    Scroll    — zoom in/out")
    print(f"    Drag node — reposition")
    print(f"    Click     — select + highlight connections")
    print(f"    Hover     — full tooltip")
    print(f"    ⊞ Fit all — reset view")
    print(f"  ─────────────────────────────────────────\n")

    if not args.no_open:
        webbrowser.open(output_path.resolve().as_uri())
        print(f"  Opened in browser.\n")


if __name__ == "__main__":
    main()
