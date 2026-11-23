
import socket
import ssl
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

uri = os.getenv("NEO4J_URI")
host = urlparse(uri).hostname

print("Aura hostname:", host)

try:
    context = ssl.create_default_context()

    with socket.create_connection(
        (host, 7687), timeout=15
    ) as connection:

        with context.wrap_socket(
            connection, server_hostname=host
        ) as secure_connection:

            print("SSL connection successful!")
            print("TLS version:", secure_connection.version())

except Exception as error:
    print("SSL connection failed:")
    print(type(error).__name__, str(error))
