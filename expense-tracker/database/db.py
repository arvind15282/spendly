import sqlite3
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    db.commit()


def seed_db():
    db = get_db()
    db.executescript("""
        INSERT OR IGNORE INTO users (name, email, password_hash) VALUES
            ('Priya Sharma', 'priya@example.com', 'hashed_pw_1'),
            ('Rahul Mehta',  'rahul@example.com', 'hashed_pw_2');

        INSERT OR IGNORE INTO expenses (user_id, amount, category, description, date) VALUES
            (1, 450.00,  'Food',   'Lunch at Swiggy',       '2025-05-01'),
            (1, 1200.00, 'Bills',  'Electricity bill',      '2025-05-03'),
            (1, 350.00,  'Travel', 'Ola cab to office',     '2025-05-05'),
            (1, 800.00,  'Food',   'Grocery run',           '2025-05-08'),
            (2, 2500.00, 'Bills',  'Internet subscription', '2025-05-02'),
            (2, 600.00,  'Travel', 'Petrol',                '2025-05-06'),
            (2, 150.00,  'Food',   'Tea and snacks',        '2025-05-09');
    """)
    db.commit()
