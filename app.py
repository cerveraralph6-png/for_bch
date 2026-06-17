from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import mysql.connector
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "bch_secret_key_123"

# --- MYSQL CONFIGURATION ---
# --- MYSQL CONFIGURATION FOR XAMPP ---
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'port': 3306,
    'password': '',  # XAMPP default MySQL password is empty
    'database': 'bch_database'
}

def get_db():
    """Establishes a connection to the MySQL database."""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    return conn

def init_db():
    """Initializes table schemas in MySQL with optimal data types."""
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Users Table (VARCHAR types with size limits for index key safety)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_number VARCHAR(100) UNIQUE,
        full_name VARCHAR(255), 
        passkey VARCHAR(255) UNIQUE, 
        role VARCHAR(100)
    )''')
    
    # Seed default Admin account (using MySQL INSERT IGNORE syntax)
    cursor.execute("""
        INSERT IGNORE INTO users (id, id_number, full_name, passkey, role) 
        VALUES (1, '0000', 'System Admin', 'bch@admin123', 'admin')
    """)
    
    # 2. Updated 21-Column Registry Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS city_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Date_Received VARCHAR(100), 
        Time_Received VARCHAR(100), 
        Type VARCHAR(100), 
        Proponent VARCHAR(255), 
        Subject TEXT, 
        Subject_Description TEXT, 
        Subject_Notation TEXT, 
        Committee_Referred VARCHAR(255), 
        Indorsement1 VARCHAR(255), 
        Date_Indorsed1 VARCHAR(100), 
        Com_Rep_Nr VARCHAR(100), 
        Com_Rep VARCHAR(255), 
        Com_Rep_Date_Received VARCHAR(100), 
        Com_Rep_Time_Received VARCHAR(100), 
        Item_Nr VARCHAR(100), 
        Agenda_Date VARCHAR(100), 
        Action_Taken VARCHAR(255), 
        Indorsement2 VARCHAR(255), 
        Indorsement2_Date VARCHAR(100), 
        Remarks TEXT, 
        Folder VARCHAR(255)
    )''')

    # 3. Events Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50),
        event_name VARCHAR(255) NOT NULL,
        event_date VARCHAR(100),
        event_time VARCHAR(100),
        location VARCHAR(255),
        status VARCHAR(50) DEFAULT 'pending'
    )''')

    conn.commit()
    cursor.close()
    conn.close()

# Initialize the database structures on startup
init_db()


# --- AUTHENTICATION ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Replaced SQLite ? with MySQL %s placeholders
    cursor.execute("SELECT * FROM users WHERE passkey = %s", (data.get('passkey', ''),))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user['id']
        session['full_name'] = user['full_name']
        session['role'] = user['role']
        return jsonify({"status": "success", "redirect": "/dashboard"})
    return jsonify({"status": "error", "message": "Invalid Passkey"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# --- DASHBOARD (ADMIN HUB) ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', 
                           user_name=session.get('full_name'), 
                           date=datetime.now().strftime('%B %d, %Y'))


# --- TOOL PAGES ---

@app.route('/registry')
def registry():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('registry.html')

@app.route('/events')
def events():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('events.html')

@app.route('/accounts')
def accounts():
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_number, full_name, role FROM users")
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('Accounts.html', accounts=users)

@app.route('/resources')
def resources():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('resources.html')


# --- ACCOUNTS MANAGEMENT API ---

@app.route('/create-account', methods=['POST'])
def create_account():
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    full_name = request.form.get('full_name')
    id_number = request.form.get('id_number')
    passkey = request.form.get('passkey')
    role = request.form.get('role')

    if full_name and id_number and passkey and role:
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (id_number, full_name, passkey, role)
                VALUES (%s, %s, %s, %s)
            ''', (id_number, full_name, passkey, role))
            conn.commit()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('accounts'))

@app.route('/edit-account', methods=['POST'])
def edit_account():
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    original_id_number = request.form.get('original_id_number')
    full_name = request.form.get('full_name')
    id_number = request.form.get('id_number')
    passkey = request.form.get('passkey')
    role = request.form.get('role')

    if full_name and id_number and role and original_id_number:
        conn = get_db()
        cursor = conn.cursor()
        try:
            if passkey:
                cursor.execute('''
                    UPDATE users 
                    SET id_number = %s, full_name = %s, passkey = %s, role = %s
                    WHERE id_number = %s
                ''', (id_number, full_name, passkey, role, original_id_number))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET id_number = %s, full_name = %s, role = %s
                    WHERE id_number = %s
                ''', (id_number, full_name, role, original_id_number))
            conn.commit()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('accounts'))

@app.route('/delete-account/<id_number>', methods=['POST'])
def delete_account(id_number):
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id_number = %s", (id_number,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('accounts'))


# --- REGISTRY API ---

@app.route('/api/records', methods=['GET'])
def get_records():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    search = request.args.get('search', '')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if search:
        query = """
            SELECT * FROM city_records 
            WHERE Proponent LIKE %s OR Subject LIKE %s OR Folder LIKE %s OR Action_Taken LIKE %s 
            ORDER BY id DESC
        """
        like_search = f'%{search}%'
        cursor.execute(query, (like_search, like_search, like_search, like_search))
    else:
        cursor.execute("SELECT * FROM city_records ORDER BY id DESC")
        
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)

@app.route('/api/records', methods=['POST'])
def save_record():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        record_id = data.get('id')

        fields = [
            'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
            'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
            'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
            'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
            'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
        ]

        values = [data.get(field, '') for field in fields]
        conn = get_db()
        cursor = conn.cursor()

        if record_id:
            # Replaced with %s syntax for MySQL
            set_clause = ", ".join([f"{field} = %s" for field in fields])
            values.append(record_id)
            cursor.execute(f"UPDATE city_records SET {set_clause} WHERE id = %s", values)
        else:
            placeholders = ", ".join(["%s"] * len(fields))
            cols = ", ".join(fields)
            cursor.execute(f"INSERT INTO city_records ({cols}) VALUES ({placeholders})", values)

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success"})
        
    except Exception as e:
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/delete-record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM city_records WHERE id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success"})


# --- EVENTS API ---

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY event_date ASC")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
def save_event():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO events (category, event_name, event_date, event_time, location) 
                    VALUES (%s, %s, %s, %s, %s)''', 
                 (data['category'], data['event_name'], data['event_date'], data['event_time'], data['location']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success"})


# --- CSV UTILITY EXPORTS & IMPORTS ---

@app.route('/api/import_csv', methods=['POST'])
def import_csv():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file."}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({"status": "error", "message": "Please upload a valid CSV file."}), 400

    try:
        file_bytes = file.stream.read()
        try:
            decoded_content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            decoded_content = file_bytes.decode("windows-1252")

        import io
        import csv
        stream = io.StringIO(decoded_content, newline=None)
        csv_reader = csv.DictReader(stream)

        if csv_reader.fieldnames:
            csv_reader.fieldnames = [name.strip() for name in csv_reader.fieldnames]

        fields = [
            'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
            'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
            'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
            'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
            'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
        ]

        records_inserted = 0
        conn = get_db()
        cursor = conn.cursor()

        for row in csv_reader:
            values = [row.get(field, '').strip() if row.get(field) is not None else '' for field in fields]
            if any(values):
                placeholders = ", ".join(["%s"] * len(fields))
                cols = ", ".join(fields)
                cursor.execute(f"INSERT INTO city_records ({cols}) VALUES ({placeholders})", values)
                records_inserted += 1

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success", 
            "message": f"Successfully imported {records_inserted} records into MySQL database."
        })

    except Exception as e:
        print("CSV Import Error:", str(e))
        return jsonify({"status": "error", "message": f"Parsing failed: {str(e)}"}), 500

@app.route('/api/export_csv')
def export_csv():
    conn = get_db()
    # Pandas seamlessly queries MySQL connections using standard SQL syntax
    df = pd.read_sql_query("SELECT * FROM city_records", conn)
    conn.close()
    file_path = "BCH_Registry_Export.csv"
    df.to_csv(file_path, index=False)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    # Change host to '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)