import webview
import threading
import time
from app import app

# Function to run the Flask server in the background
def start_flask():
    # Change host to '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # 1. Start Flask in a separate thread
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    # 2. Give the server a second to start
    time.sleep(1)

    # 3. Create the window
    webview.create_window(
        'Baguio City Hall | Management System', 
        'http://localhost/CouncilApp/templates/index.html',
        width=1200,
        height=800,
        resizable=True,
        confirm_close=True
    )
    
    # 4. Launch the app
    webview.start()