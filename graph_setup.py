from database import Neo4jConnection

# This script creates the sample graph. It intentionally clears the
# selected Neo4j database first; do not run against a database with data
# you need to keep.
CREATE_GRAPH = """
MATCH (n)
DETACH DELETE n;

CREATE
(s2:Supplier {
    name: "Lithium Mining Co",
    tier: 2,
    risk_score: 85
}),
(s1:Supplier {
    name: "Battery Materials Ltd",
    tier: 1,
    risk_score: 70
}),
(s3:Supplier {
    name: "ChipTech Electronics",
    tier: 1,
    risk_score: 25
}),
(c1:Component {name: "Lithium Battery"}),
(c2:Component {name: "Microcontroller"}),
(p:Product {name: "Electric Vehicle"}),
(pl:Plant {name: "Pune Plant", city: "Pune"}),
(co1:Country {name: "Australia"}),
(co2:Country {name: "China"}),
(co3:Country {name: "India"}),
(sh1:Shipment {
    shipment_id: "Shipment-101",
    status: "Delayed"
}),
(sh2:Shipment {
    shipment_id: "Shipment-102",
    status: "Delivered"
}),
(s2)-[:SUPPLIES]->(s1),
(s1)-[:SUPPLIES]->(c1),
(s3)-[:SUPPLIES]->(c2),
(c1)-[:USED_IN]->(p),
(c2)-[:USED_IN]->(p),
(p)-[:MANUFACTURED_AT]->(pl),
(s2)-[:LOCATED_IN]->(co1),
(s1)-[:LOCATED_IN]->(co2),
(s3)-[:LOCATED_IN]->(co3),
(sh1)-[:CONTAINS]->(c1),
(sh2)-[:CONTAINS]->(c2),
(sh1)-[:DESTINED_FOR]->(pl),
(sh2)-[:DESTINED_FOR]->(pl)
"""

def create_supply_chain_graph(db):
    db.execute_query(CREATE_GRAPH)
    print("Supply-chain graph created successfully (11 nodes, 14 relationships).")

if __name__ == "__main__":
    db = Neo4jConnection()
    try:
        create_supply_chain_graph(db)
    finally:
        db.close()
