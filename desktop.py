import threading
import socket
import webview
from concurrent.futures import ThreadPoolExecutor

PORT = 5000

def start_flask():
    """Starts the local Flask server. Lazy imported to prevent client-side crashes."""
    try:
        from app import app  # Imported only when acting as Host
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)
    except ImportError as e:
        print(f"Error starting local server: {e}")
        print("Please ensure Flask and its dependencies are installed on this host machine.")

def check_ip_port(ip, port):
    """Checks if a specific IP is active on port 5000."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.15)  # Fast timeout for local subnets
            s.connect((ip, port))
        return ip
    except Exception:
        return None

def discover_host_ip():
    """Automatically scans the local network subnet to locate the active host."""
    # 1. Get the current computer's local network IP
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

    # 2. Extract subnet prefix (e.g., '192.168.6.X' -> '192.168.6.')
    ip_parts = local_ip.split('.')
    subnet_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."
    print(f"Your IP: {local_ip} | Scanning subnet: {subnet_prefix}0/24...")

    # 3. Generate all 254 possible local IP addresses
    target_ips = [f"{subnet_prefix}{i}" for i in range(1, 255) if f"{subnet_prefix}{i}" != local_ip]

    # 4. Scan all IPs concurrently using 50 background worker threads
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda ip: check_ip_port(ip, PORT), target_ips)

    for result in results:
        if result:
            return result  # Returns the IP of the running server
    return None

if __name__ == '__main__':
    # Automatically scan the network for an active server
    active_host_ip = discover_host_ip()
    
    if active_host_ip:
        # CLIENT MODE: Active server found on the network
        print(f"Active server discovered at http://{active_host_ip}:{PORT}")
        target_url = f"http://{active_host_ip}:{PORT}"
    else:
        # HOST MODE: No active server found on the network; start local Flask server
        print("No active server found on network. Launching in Host Mode...")
        flask_thread = threading.Thread(target=start_flask)
        flask_thread.daemon = True
        flask_thread.start()
        target_url = f"http://127.0.0.1:{PORT}"

    # Open the native desktop window
    webview.create_window(
        title='Baguio City Hall | Management System', 
        url=target_url,
        width=1200,
        height=800
    )
    webview.start()