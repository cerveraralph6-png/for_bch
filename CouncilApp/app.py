from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import sqlite3
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "bch_secret_key_123"

# --- DATABASE SETUP ---
def get_db():
    conn = sqlite3.connect('bch_local.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    
    # 1. Users Table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT, passkey TEXT UNIQUE, role TEXT
    )''')
    conn.execute("INSERT OR IGNORE INTO users (id, full_name, passkey, role) VALUES (1, 'System Admin', 'bch@admin123', 'admin')")
    
    # 2. The 21-Column Registry Table
    conn.execute('''CREATE TABLE IF NOT EXISTS city_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_Received TEXT, Time_Received TEXT, Ref_No TEXT,
        Type TEXT, Proponent TEXT, Subject TEXT,
        Subject_Description TEXT, Subject_Notation TEXT, Committee_Referred TEXT,
        Indorsement1 TEXT, Date_Indorsed1 TEXT, Com_Rep_Nr TEXT,
        Com_Rep TEXT, Com_Rep_Date_Received TEXT, Item_Nr TEXT,
        Agenda_Date TEXT, Action_Taken TEXT, Indorsement2 TEXT,
        Indorsement2_Date TEXT, Remarks TEXT, Folder TEXT
    )''')

    # 3. FIXED: Events Table (Inside init_db now)
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

# Initialize the database when the app starts
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

@app.route('/accounts')
def accounts():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('accounts.html')

@app.route('/resources')
def resources():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('resources.html')



# --- REGISTRY API ---

@app.route('/api/records', methods=['GET'])
def get_records():
    search = request.args.get('search', '')
    conn = get_db()
    if search:
        query = "SELECT * FROM city_records WHERE Ref_No LIKE ? OR Proponent LIKE ? OR Subject LIKE ? ORDER BY id DESC"
        records = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        records = conn.execute("SELECT * FROM city_records ORDER BY id DESC LIMIT 100").fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/records', methods=['POST'])
def save_record():
    data = request.json
    record_id = data.pop('id', None)
    columns = list(data.keys())
    values = list(data.values())
    conn = get_db()
    if record_id:
        set_clause = ", ".join([f"{col} = ?" for col in columns])
        values.append(record_id)
        conn.execute(f"UPDATE city_records SET {set_clause} WHERE id = ?", values)
    else:
        placeholders = ", ".join(["?"] * len(values))
        cols = ", ".join(columns)
        conn.execute(f"INSERT INTO city_records ({cols}) VALUES ({placeholders})", values)
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


if __name__ == '__main__':
    app.run(port=5000)