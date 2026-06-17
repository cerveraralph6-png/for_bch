import threading
import socket
import webview
from concurrent.futures import ThreadPoolExecutor

PORT = 5000

def start_flask():
    """Starts the local Flask server. Lazy imported to prevent client-side crashes."""
    try:
        from app import app
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
    except ImportError as e:
        print(f"Error starting local server: {e}")
        print("Ensure Flask and MySQL dependencies are installed to run as Host.")

def check_ip_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.12)  # Fast local subnet timeout
            s.connect((ip, port))
        return ip
    except Exception:
        return None

def discover_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    if local_ip == '127.0.0.1':
        return None

    ip_parts = local_ip.split('.')
    subnet_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."
    print(f"Your IP: {local_ip} | Scanning subnet: {subnet_prefix}0/24...")

    target_ips = [f"{subnet_prefix}{i}" for i in range(1, 255) if f"{subnet_prefix}{i}" != local_ip]

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda ip: check_ip_port(ip, PORT), target_ips)

    for result in results:
        if result:
            return result
    return None

if __name__ == '__main__':
    active_host_ip = discover_host_ip()
    
    if active_host_ip:
        print(f"Active server automatically discovered at http://{active_host_ip}:{PORT}")
        target_url = f"http://{active_host_ip}:{PORT}"
    else:
        print("\n[!] No active server found automatically on your network.")
        print("------------------------------------------------------------------")
        print("1. Enter 'host' to launch the local database server on this machine.")
        print("2. Or, type the manual IP of the host machine to attempt connection.")
        print("------------------------------------------------------------------")
        
        user_choice = input("Your choice: ").strip()
        
        if user_choice.lower() == 'host':
            print("Launching in Host Mode...")
            flask_thread = threading.Thread(target=start_flask)
            flask_thread.daemon = True
            flask_thread.start()
            target_url = f"http://127.0.0.1:{PORT}"
        else:
            # Strip out http:// or trailing ports if entered by mistake
            manual_ip = user_choice.replace("http://", "").split(":")[0]
            print(f"Attempting manual connection to http://{manual_ip}:{PORT}...")
            target_url = f"http://{manual_ip}:{PORT}"

    # Open native window
    webview.create_window(
        title='Baguio City Hall | Management System', 
        url=target_url,
        width=1200,
        height=800
    )
    webview.start()