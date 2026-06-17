from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import sqlite3
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "bch_secret_key_123"

# --- DATABASE SETUP ---# --- DATABASE SETUP ---
def get_db():
    conn = sqlite3.connect('bch_local.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    
    # 1. Users Table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_number TEXT UNIQUE,
        full_name TEXT, 
        passkey TEXT UNIQUE, 
        role TEXT
    )''')
    conn.execute("INSERT OR IGNORE INTO users (id, id_number, full_name, passkey, role) VALUES (1, '0000', 'System Admin', 'bch@admin123', 'admin')")
    
    # 2. Updated 21-Column Registry Table (as requested)
    conn.execute('''CREATE TABLE IF NOT EXISTS city_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_Received TEXT, 
        Time_Received TEXT, 
        Type TEXT, 
        Proponent TEXT, 
        Subject TEXT, 
        Subject_Description TEXT, 
        Subject_Notation TEXT, 
        Committee_Referred TEXT, 
        Indorsement1 TEXT, 
        Date_Indorsed1 TEXT, 
        Com_Rep_Nr TEXT, 
        Com_Rep TEXT, 
        Com_Rep_Date_Received TEXT, 
        Com_Rep_Time_Received TEXT, 
        Item_Nr TEXT, 
        Agenda_Date TEXT, 
        Action_Taken TEXT, 
        Indorsement2 TEXT, 
        Indorsement2_Date TEXT, 
        Remarks TEXT, 
        Folder TEXT
    )''')

    # 3. Events Table
    conn.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT CHECK(category IN ('Seminar', 'Training', 'Others')),
        event_name TEXT NOT NULL,
        event_date TEXT,
        event_time TEXT,
        location TEXT,
        status TEXT DEFAULT 'pending'
    )''')

    conn.commit()
    conn.close()

# Run the database initialization
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
    user = conn.execute("SELECT * FROM users WHERE passkey = ?", (data.get('passkey', ''),)).fetchone()
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

# --- TOOL PAGES ---

@app.route('/accounts')
def accounts():
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    # Fetch all users from the database
    conn = get_db()
    users = conn.execute("SELECT id_number, full_name, role FROM users").fetchall()
    conn.close()
    
    # Note: Using 'Accounts.html' (Capital A) to match your exact file name
    return render_template('Accounts.html', accounts=users)

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
        try:
            conn.execute('''
                INSERT INTO users (id_number, full_name, passkey, role)
                VALUES (?, ?, ?, ?)
            ''', (id_number, full_name, passkey, role))
            conn.commit()
        except sqlite3.IntegrityError:
            # Handles duplicate passkey or duplicate ID number
            pass
        finally:
            conn.close()

    return redirect(url_for('accounts'))

@app.route('/edit-account', methods=['POST'])
def edit_account():
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    # Retrieve form data
    original_id_number = request.form.get('original_id_number')
    full_name = request.form.get('full_name')
    id_number = request.form.get('id_number')
    passkey = request.form.get('passkey')
    role = request.form.get('role')

    if full_name and id_number and role and original_id_number:
        conn = get_db()
        try:
            if passkey:  # If a passkey is provided, update everything including password
                conn.execute('''
                    UPDATE users 
                    SET id_number = ?, full_name = ?, passkey = ?, role = ?
                    WHERE id_number = ?
                ''', (id_number, full_name, passkey, role, original_id_number))
            else:  # If passkey is left blank, preserve the existing password
                conn.execute('''
                    UPDATE users 
                    SET id_number = ?, full_name = ?, role = ?
                    WHERE id_number = ?
                ''', (id_number, full_name, role, original_id_number))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            conn.close()

    return redirect(url_for('accounts'))


@app.route('/delete-account/<id_number>', methods=['POST'])
def delete_account(id_number):
    if 'user_id' not in session: 
        return redirect(url_for('index'))
    
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id_number = ?", (id_number,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('accounts'))

@app.route('/resources')
def resources():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('resources.html')



# --- REGISTRY API ---

# --- UPDATE IN APP.PY ---

@app.route('/api/records', methods=['GET'])
def get_records():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    search = request.args.get('search', '')
    conn = get_db()
    
    if search:
        query = """
            SELECT * FROM city_records 
            WHERE Proponent LIKE ? OR Subject LIKE ? OR Folder LIKE ? OR Action_Taken LIKE ? 
            ORDER BY id DESC
        """
        like_search = f'%{search}%'
        records = conn.execute(query, (like_search, like_search, like_search, like_search)).fetchall()
    else:
        # Removed 'LIMIT 100' so the frontend can paginate through all historic records
        records = conn.execute("SELECT * FROM city_records ORDER BY id DESC").fetchall()
        
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/records', methods=['POST'])
def save_record():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        record_id = data.get('id')  # Detects if editing an existing entry

        # The 21 schema columns
        fields = [
            'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
            'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
            'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
            'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
            'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
        ]

        # Gather values dynamically from the JSON payload (defaulting to empty string if missing)
        values = [data.get(field, '') for field in fields]
        conn = get_db()

        if record_id:
            # Edit Mode: Update existing record
            set_clause = ", ".join([f"{field} = ?" for field in fields])
            values.append(record_id)
            conn.execute(f"UPDATE city_records SET {set_clause} WHERE id = ?", values)
        else:
            # Create Mode: Insert new record
            placeholders = ", ".join(["?"] * len(fields))
            cols = ", ".join(fields)
            conn.execute(f"INSERT INTO city_records ({cols}) VALUES ({placeholders})", values)

        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
        
    except Exception as e:
        # Logs database errors (like missing tables or columns) directly to your Python terminal
        print("Database Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/delete-record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    conn.execute("DELETE FROM city_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# --- EVENTS API ---

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db()
    events = conn.execute("SELECT * FROM events ORDER BY event_date ASC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in events])

@app.route('/api/events', methods=['POST'])
def save_event():
    data = request.json
    conn = get_db()
    conn.execute('''INSERT INTO events (category, event_name, event_date, event_time, location) 
                    VALUES (?, ?, ?, ?, ?)''', 
                 (data['category'], data['event_name'], data['event_date'], data['event_time'], data['location']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/export_csv')
def export_csv():
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM city_records", conn)
    conn.close()
    file_path = "BCH_Registry_Export.csv"
    df.to_csv(file_path, index=False)
    return send_file(file_path, as_attachment=True)

# --- ADD THIS TO APP.PY ---
import io
import csv
from flask import jsonify, request, session
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
        # Read the raw file bytes
        file_bytes = file.stream.read()
        
        # Try decoding as standard UTF-8; fallback to windows-1252 (Excel compatible) if it fails
        try:
            decoded_content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            decoded_content = file_bytes.decode("windows-1252")

        # Convert the decoded string to an in-memory text stream
        stream = io.StringIO(decoded_content, newline=None)
        csv_reader = csv.DictReader(stream)

        # Normalize header column whitespace
        if csv_reader.fieldnames:
            csv_reader.fieldnames = [name.strip() for name in csv_reader.fieldnames]

        # The 21 schema columns to match and insert
        fields = [
            'Date_Received', 'Time_Received', 'Type', 'Proponent', 'Subject',
            'Subject_Description', 'Subject_Notation', 'Committee_Referred', 'Indorsement1',
            'Date_Indorsed1', 'Com_Rep_Nr', 'Com_Rep', 'Com_Rep_Date_Received',
            'Com_Rep_Time_Received', 'Item_Nr', 'Agenda_Date', 'Action_Taken',
            'Indorsement2', 'Indorsement2_Date', 'Remarks', 'Folder'
        ]

        records_inserted = 0
        conn = get_db()

        for row in csv_reader:
            # Map values to fields. If a column is missing in the CSV, defaults to empty string.
            values = [row.get(field, '').strip() if row.get(field) is not None else '' for field in fields]
            
            # Insert row only if at least one column is filled (prevents empty row inserts)
            if any(values):
                placeholders = ", ".join(["?"] * len(fields))
                cols = ", ".join(fields)
                conn.execute(f"INSERT INTO city_records ({cols}) VALUES ({placeholders})", values)
                records_inserted += 1

        conn.commit()
        conn.close()

        return jsonify({
            "status": "success", 
            "message": f"Successfully imported {records_inserted} records into the database."
        })

    except Exception as e:
        print("CSV Import Error:", str(e))
        return jsonify({"status": "error", "message": f"Parsing failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)