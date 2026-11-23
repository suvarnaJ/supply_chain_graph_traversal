# Mini Supply Chain Graph Traversal (Python + Neo4j)

## What this project demonstrates
- Supplier, Component, Product, Plant, Shipment and Country nodes
- Tier-2 supplier -> Tier-1 supplier -> Component dependency
- 15 Cypher queries: single-hop, multi-hop, reverse direction, filters,
  aggregation, paths and variable-length traversal
- Optional NetworkX / Matplotlib visualization

## Requirements
- Python 3.10+
- Neo4j Desktop local database, or a Neo4j Aura database
- A running Neo4j database with Bolt connectivity enabled

## Setup on Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set the URI, username, password and database for your Neo4j instance.
For a local Neo4j Desktop database, `bolt://localhost:7687` is a common URI.
Do not share or commit your `.env` file.

## Run

```powershell
python main.py
```

This creates the sample graph and runs all 15 traversal queries.

To visualize the graph after setup:

```powershell
python visualize_graph.py
```

## Important safety note
`graph_setup.py` starts by running `MATCH (n) DETACH DELETE n`. This deletes
all nodes and relationships in the selected database. Use a dedicated,
empty practice database, or remove that statement and use a scoped cleanup
if you need to preserve existing data.

## Sample graph path

Lithium Mining Co (Tier 2)
  -[:SUPPLIES]->
Battery Materials Ltd (Tier 1)
  -[:SUPPLIES]->
Lithium Battery
  -[:USED_IN]->
Electric Vehicle
  -[:MANUFACTURED_AT]->
Pune Plant

## Files
- `database.py`: Neo4j connection helper
- `graph_setup.py`: creates the example graph
- `traversal_queries.py`: 15 traversal queries and runner
- `main.py`: runs setup and queries
- `visualize_graph.py`: fetches graph data and plots it
- `.env.example`: connection settings template
