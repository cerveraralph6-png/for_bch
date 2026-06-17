# ==========================================
#   RUN THIS ON COMPUTER A (THE HOST) ONLY
# ==========================================
import threading
import webview
from app import app  # Imports your Flask app

def start_flask():
    """Starts the Flask server on port 5000, listening on all network interfaces."""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Start Flask in a background thread so other computers can connect
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 2. Open the window pointing to localhost
    webview.create_window(
        title='Baguio City Hall | Management System (HOST)', 
        url='http://127.0.0.1:5000',
        width=1200,
        height=800
    )
    webview.start()