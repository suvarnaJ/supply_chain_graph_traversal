
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

print("URI:", URI)
print("Username loaded:", bool(USERNAME))
print("Password loaded:", bool(PASSWORD))

if not all([URI, USERNAME, PASSWORD]):
    raise ValueError("Missing Neo4j configuration. Check your .env file.")

try:
    with GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    ) as driver:

        driver.verify_connectivity()

        with driver.session(database=DATABASE) as session:
            result = session.run("RETURN 'Aura Connected Successfully!' AS message")
            print(result.single()["message"])

except Exception as error:
    print("Connection failed:")
    print(type(error).__name__, str(error))
