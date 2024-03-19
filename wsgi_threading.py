import os
from gevent import pywsgi
from dotenv import load_dotenv
from geventwebsocket.handler import WebSocketHandler
from concurrent.futures import ThreadPoolExecutor
from Whisper import app  # Asumiendo que 'Whisper' es un módulo personalizado correctamente importado

# Get environment variables
load_dotenv()

def start_server():
    """
    Create and start a WSGI server using Gevent and WebSocketHandler.
    """
    host = os.environ['HOST']
    port = int(os.environ['PORT'])
    server = pywsgi.WSGIServer((host, port), app, handler_class=WebSocketHandler)

    # Print information with the address where the server is deployed
    print(f"Server deployed at: {host}:{port}")

    # Start the server to continuously listen for incoming requests
    server.serve_forever()

if __name__ == "__main__":
    try:
        max_workers = int(os.environ.get('MAX_WORKERS', 1))
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Start the server in a separate thread
            executor.submit(start_server)
    except KeyboardInterrupt:
        # Handle a keyboard interruption (Ctrl+C) to cleanly close the server
        print("Server stopped by the user.")
    except Exception as e:
        # Print any other error
        print(f"Error: {e}")
