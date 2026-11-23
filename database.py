import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")


class Neo4jConnection:
    def __init__(self):
        if not PASSWORD:
            raise ValueError(
                "NEO4J_PASSWORD is missing. Copy .env.example to .env "
                "and enter your Neo4j password."
            )
        self.driver = GraphDatabase.driver(
            URI, auth=(USERNAME, PASSWORD)
        )
        self.driver.verify_connectivity()
        print("Connected to Neo4j successfully!")

    def execute_query(self, query, parameters=None):
        with self.driver.session(database=DATABASE) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
        print("Neo4j connection closed.")
