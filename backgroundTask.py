import os
import threading
import time
import http.server
import socketserver

# Background task
def background_task():
    while True:
        print("Background task is running...")
        time.sleep(5)

# Start background task
threading.Thread(target=background_task, daemon=True).start()

# Get port from environment
port = int(os.environ.get("PORT", 8000))

# Start HTTP server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving HTTP on port {port}")
    httpd.serve_forever()
