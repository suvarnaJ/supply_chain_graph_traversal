from database import Neo4jConnection
from graph_setup import create_supply_chain_graph
from traversal_queries import run_all_queries

def main():
    db = None
    try:
        db = Neo4jConnection()
        create_supply_chain_graph(db)
        run_all_queries(db)
    except Exception as exc:
        print(f"Application error: {exc}")
    finally:
        if db is not None:
            db.close()

if __name__ == "__main__":
    main()
