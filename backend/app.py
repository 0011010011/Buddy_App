import sqlite3
from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='../frontend')
DB = "buddy.db"

def db():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            species TEXT,
            breed TEXT,
            size TEXT,
            age TEXT,
            gender TEXT,
            description TEXT,
            image TEXT,
            shelter TEXT,
            shelter_email TEXT
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS shelters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            address TEXT,
            description TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS adopter_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            garden TEXT,
            large_home TEXT,
            kids TEXT,
            animal_friendly TEXT DEFAULT 'unknown',
            hours_away TEXT,
            free_text TEXT,
            paid INTEGER DEFAULT 0,
            amount REAL DEFAULT 23.00
        )
    """)
    connection.commit()
    connection.close()

init_db()

# Serve Frontend Files
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# API Endpoints
@app.route("/api/animals")
def animals():
    connection = db()
    rows = [dict(row) for row in connection.execute("SELECT * FROM animals ORDER BY id DESC")]
    connection.close()
    return jsonify(rows)

@app.route("/api/shelters")
def shelter_list():
    connection = db()
    rows = [dict(row) for row in connection.execute("SELECT * FROM shelters ORDER BY id DESC")]
    connection.close()
    return jsonify(rows)

@app.route("/api/shelter", methods=["POST"])
def add_shelter():
    data = request.json or {}
    connection = db()
    connection.execute(
        """
        INSERT INTO shelters (name, email, address, description)
        VALUES (?, ?, ?, ?)
        """,
        (data.get("name"), data.get("email"), data.get("address"), data.get("description"))
    )
    connection.commit()
    connection.close()
    return jsonify({"success": True})

@app.route("/api/animal", methods=["POST"])
def add_animal():
    data = request.json or {}
    connection = db()
    connection.execute(
        """
        INSERT INTO animals
        (name, species, breed, size, age, gender, description, image, shelter, shelter_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("name"), data.get("species"), data.get("breed"),
            data.get("size"), data.get("age"), data.get("gender"),
            data.get("description"), data.get("image"),
            data.get("shelter"), data.get("shelter_email")
        )
    )
    connection.commit()
    connection.close()
    return jsonify({"success": True})

@app.route("/api/animal/<int:id>", methods=["DELETE"])
def delete_animal(id):
    connection = db()
    connection.execute("DELETE FROM animals WHERE id = ?", (id,))
    connection.commit()
    connection.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    