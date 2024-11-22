# db.py
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('meetings.db', check_same_thread=False)

# Create a cursor
cursor = conn.cursor()

# Create table for meetings
cursor.execute('''CREATE TABLE IF NOT EXISTS meetings (
                    meeting_id TEXT PRIMARY KEY,
                    discussion_text TEXT
                  )''')
conn.commit()

# Function to store meeting data
def store_meeting_text(meeting_id, discussion_points):
    text = "\n".join(discussion_points)
    cursor.execute("INSERT INTO meetings (meeting_id, discussion_text) VALUES (?, ?)", (meeting_id, text))
    conn.commit()

# Function to retrieve meeting data
def retrieve_meeting_text(meeting_id):
    cursor.execute("SELECT discussion_text FROM meetings WHERE meeting_id = ?", (meeting_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return f"No data found for meeting ID {meeting_id}"


import sqlite3

conn = sqlite3.connect('meetings2.db')
cursor = conn.cursor()

# Create the table for meetings
cursor.execute('''CREATE TABLE IF NOT EXISTS meetings2 (
    meeting_id TEXT PRIMARY KEY,
    discussion_points TEXT
)''')

# Function to save discussion points
def save_discussion_points(meeting_id, discussion_points):
    cursor.execute("INSERT INTO meetings2 (meeting_id, discussion_points) VALUES (?, ?)", 
                   (meeting_id, '\n'.join(discussion_points)))
    conn.commit()

# Function to load discussion points
def load_discussion_points(meeting_id):
    cursor.execute("SELECT discussion_points FROM meetings2 WHERE meeting_id = ?", (meeting_id,))
    result = cursor.fetchone()
    return result[0].split('\n') if result else []

# Close the database connection when the app shuts down
def close_db():
    if conn:
        conn.close()

