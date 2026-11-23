# 15 Cypher graph-traversal queries for the supply-chain graph.

QUERIES = {
    "1 - Retrieve all suppliers": """
        MATCH (s:Supplier)
        RETURN s.name AS Supplier, s.tier AS Tier,
               s.risk_score AS RiskScore
        ORDER BY Supplier
    """,

    "2 - Single-hop: supplier to component": """
        MATCH (s:Supplier)-[:SUPPLIES]->(c:Component)
        RETURN s.name AS Supplier, c.name AS Component
    """,

    "3 - Single-hop: component to product": """
        MATCH (c:Component)-[:USED_IN]->(p:Product)
        RETURN c.name AS Component, p.name AS Product
    """,

    "4 - Single-hop: product to plant": """
        MATCH (p:Product)-[:MANUFACTURED_AT]->(pl:Plant)
        RETURN p.name AS Product, pl.name AS Plant
    """,

    # Two SUPPLIES hops are required because Tier-2 supplies Tier-1,
    # and Tier-1 supplies the Component.
    "5 - Multi-hop: Tier-2 supplier to plant": """
        MATCH path =
          (s:Supplier {name: $supplier_name})
          -[:SUPPLIES*2]->
          (c:Component)
          -[:USED_IN]->
          (p:Product)
          -[:MANUFACTURED_AT]->
          (pl:Plant)
        RETURN path
    """,

    "6 - Tier-2 supplier to Tier-1 supplier": """
        MATCH (tier2:Supplier {tier: 2})-[:SUPPLIES]->
              (tier1:Supplier {tier: 1})
        RETURN tier2.name AS Tier2Supplier,
               tier1.name AS Tier1Supplier
    """,

    "7 - Reverse direction: component to supplying supplier": """
        MATCH (c:Component {name: $component_name})
              <-[:SUPPLIES]-(s:Supplier)
        RETURN s.name AS Supplier, c.name AS Component
    """,

    "8 - Filter suppliers by risk score": """
        MATCH (s:Supplier)
        WHERE s.risk_score > $risk_threshold
        RETURN s.name AS Supplier, s.risk_score AS RiskScore
        ORDER BY RiskScore DESC
    """,

    "9 - Find suppliers by country": """
        MATCH (s:Supplier)-[:LOCATED_IN]->
              (c:Country {name: $country_name})
        RETURN s.name AS Supplier, c.name AS Country
    """,

    "10 - Count directly supplied components per supplier": """
        MATCH (s:Supplier)-[:SUPPLIES]->(c:Component)
        RETURN s.name AS Supplier, count(c) AS TotalComponents
        ORDER BY TotalComponents DESC
    """,

    "11 - Count products using each component": """
        MATCH (c:Component)-[:USED_IN]->(p:Product)
        RETURN c.name AS Component,
               count(DISTINCT p) AS ProductCount
    """,

    "12 - Components in delayed shipments": """
        MATCH (sh:Shipment {status: "Delayed"})-[:CONTAINS]->
              (c:Component)
        RETURN sh.shipment_id AS Shipment,
               sh.status AS Status,
               c.name AS Component
    """,

    "13 - Destination plants for delayed shipments": """
        MATCH (sh:Shipment {status: "Delayed"})-[:DESTINED_FOR]->
              (pl:Plant)
        RETURN sh.shipment_id AS Shipment, pl.name AS Plant
    """,

    "14 - Variable-length supplier dependency chain": """
        MATCH path =
          (s:Supplier {name: $supplier_name})
          -[:SUPPLIES*1..5]->
          (other:Supplier)
        RETURN path
    """,

    "15 - End-to-end supplier risk impact": """
        MATCH
          (s:Supplier {name: $supplier_name})
          -[:SUPPLIES*1..5]->
          (tier1:Supplier)
          -[:SUPPLIES]->
          (c:Component)
          -[:USED_IN]->
          (p:Product)
          -[:MANUFACTURED_AT]->
          (pl:Plant)
        RETURN DISTINCT
          s.name AS AtRiskSupplier,
          tier1.name AS DependentSupplier,
          c.name AS AffectedComponent,
          p.name AS AffectedProduct,
          pl.name AS AffectedPlant
    """
}

DEFAULT_PARAMETERS = {
    "supplier_name": "Lithium Mining Co",
    "component_name": "Lithium Battery",
    "risk_threshold": 60,
    "country_name": "Australia",
}

def run_all_queries(db):
    for title, cypher in QUERIES.items():
        print("\\n" + "=" * 72)
        print(title)
        print("=" * 72)
        try:
            records = db.execute_query(cypher, DEFAULT_PARAMETERS)
            if not records:
                print("No records found.")
            for record in records:
                # Path objects are returned as driver objects; print their
                # nodes and relationships in a readable form.
                if "path" in record:
                    path = record["path"]
                    print(" -> ".join(
                        f"{node.get('name', node.get('shipment_id', '?'))}"
                        for node in path.nodes
                    ))
                else:
                    print(record)
        except Exception as exc:
            print(f"Query failed: {exc}")
