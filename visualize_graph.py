import networkx as nx
import matplotlib.pyplot as plt
from database import Neo4jConnection

QUERY = """
MATCH (a)-[r]->(b)
RETURN
  coalesce(a.name, a.shipment_id) AS source,
  labels(a) AS source_labels,
  type(r) AS relationship,
  coalesce(b.name, b.shipment_id) AS target,
  labels(b) AS target_labels
"""

COLORS = {
    "Supplier": "orange",
    "Component": "skyblue",
    "Product": "lightgreen",
    "Plant": "salmon",
    "Country": "khaki",
    "Shipment": "plum",
}

def main():
    db = Neo4jConnection()
    try:
        records = db.execute_query(QUERY)
    finally:
        db.close()

    graph = nx.DiGraph()
    for row in records:
        source, target = row["source"], row["target"]
        source_type = row["source_labels"][0]
        target_type = row["target_labels"][0]
        graph.add_node(source, node_type=source_type)
        graph.add_node(target, node_type=target_type)
        graph.add_edge(source, target, label=row["relationship"])

    pos = nx.spring_layout(graph, seed=42, k=1.5)
    node_colors = [
        COLORS.get(graph.nodes[node]["node_type"], "lightgray")
        for node in graph.nodes
    ]

    plt.figure(figsize=(16, 10))
    nx.draw_networkx(
        graph, pos, with_labels=True, node_color=node_colors,
        node_size=2400, font_size=8, arrows=True, arrowsize=18
    )
    labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(
        graph, pos, edge_labels=labels, font_size=7
    )
    plt.title("Mini Supply Chain Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
