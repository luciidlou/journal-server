import json
import sqlite3

from models import Entry, Mood


def get_all_entries():
    """GETS the list of entries from the server"""

    with sqlite3.connect('./journal.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'],
                          row['date'])

            mood = Mood(row['mood_id'], row['label'])

            entries.append(entry.__dict__)
            entry.mood = mood.__dict__

    return json.dumps(entries)


def get_single_entry(id):
    """GETS the entry with the corresponding id"""

    with sqlite3.connect('./journal.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entries a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'],
                      data['entry'], data['mood_id'],
                      data['date'])

    return json.dumps(entry.__dict__)


def get_entries_by_search(search_term):
    """GETS a list of entries that match the search_term"""

    with sqlite3.connect('./journal.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entries a
        WHERE a.entry LIKE ?;
        """, (f'%{search_term}%', ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'],
                          row['date'])

            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    """Adds a new entry to the Entries list"""
    with sqlite3.connect('./journal.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO entries
            (concept, entry, mood_id, date)
        VALUES
            (?, ?, ?, ?)
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date']))

        id = db_cursor.lastrowid
        new_entry['id'] = id

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect('./journal.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
            WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def delete_entry(id):
    """DELETES the entry with the corresponding id"""
    with sqlite3.connect("./journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?                  
        """, (id, ))
