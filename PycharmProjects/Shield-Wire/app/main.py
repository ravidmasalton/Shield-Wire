import psycopg2
import os
from flask import Flask, jsonify

app = Flask(__name__)

# פונקציה לחיבור לבסיס הנתונים
def get_db_connection():
    conn = psycopg2.connect(
        host='db', # שם השירות ב-docker-compose
        database='shield_db',
        user='user',
        password='password'
    )
    return conn

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # יצירת טבלה אם היא לא קיימת (דימוי של רישום לוגים)
        cur.execute('CREATE TABLE IF NOT EXISTS access_logs (id serial PRIMARY KEY, access_time timestamp DEFAULT CURRENT_TIMESTAMP);')
        cur.execute('INSERT INTO access_logs (access_time) VALUES (DEFAULT);')
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Shield-Wire: Log saved to Database!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/logs')
def view_logs():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM access_logs ORDER BY access_time DESC;')
        rows = cur.fetchall() # שולף את כל השורות מהטבלה
        cur.close()
        conn.close()
        
        # נהפוך את התוצאה לרשימה של מילונים כדי שיהיה קל לקרוא
        logs = [{"id": r[0], "time": r[1].strftime("%Y-%m-%d %H:%M:%S")} for r in rows]
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)