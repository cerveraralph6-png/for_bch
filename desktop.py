# --- RUN THIS ON COMPUTER B (CLIENT) ---
import webview

if __name__ == '__main__':
    # Replace this with the physical local IP of Computer A (Host)
    HOST_IP = '192.168.6.93' 

    # Simply open the window pointing directly to the host's server
    webview.create_window(
        title='Baguio City Hall | Management System', 
        url=f'http://{HOST_IP}:5000',
        width=1200,
        height=800
    )
    webview.start()