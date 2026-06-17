import threading
import socket
import webview
from app import app  # Imports your Flask app

# --- CENTRAL CONFIGURATION ---
# Set this to the physical IP address of Computer A (the main server/database host)
HOST_IP = '192.168.1.15' 
PORT = 5000

def start_flask():
    """Starts the local Flask server to host the app and database."""
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def is_main_server_online(ip, port):
    """Checks if the main server on Computer A is already online on the network."""
    try:
        # Create a lightweight TCP socket connection test
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)  # 1.5-second timeout
            s.connect((ip, port))
        return True
    except Exception:
        return False

if __name__ == '__main__':
    print(f"Scanning for main server at http://{HOST_IP}:{PORT}...")
    
    if is_main_server_online(HOST_IP, PORT):
        # CLIENT MODE: The server is already up. Just load the viewport.
        print("Main server detected. Launching app in Client Mode...")
        target_url = f"http://{HOST_IP}:{PORT}"
    else:
        # HOST MODE: The server is not running yet. Start it locally.
        print("Main server not found. Starting local Flask server (Host Mode)...")
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()
        target_url = f"http://127.0.0.1:{PORT}"

    # Open the native desktop viewport window
    webview.create_window(
        title='Baguio City Hall | Management System', 
        url=target_url,
        width=1200,
        height=800
    )
    webview.start()