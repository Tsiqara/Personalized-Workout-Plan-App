import sqlite3

connection = sqlite3.connect("../../test_sqlite.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS exercises;")
cursor.execute("DROP TABLE IF EXISTS workouts;")
cursor.execute("DROP TABLE IF EXISTS workout_exercises;")
cursor.execute("DROP TABLE IF EXISTS workout_goals;")
cursor.execute("DROP TABLE IF EXISTS goals;")
cursor.execute("DROP TABLE IF EXISTS weight_records;")

connection.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        [username] TEXT PRIMARY KEY,
        [password] TEXT
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS exercises (
        [ID] TEXT PRIMARY KEY,
        [name] TEXT,
        [description] TEXT,
        [instructions] TEXT,
        [target_muscles] TEXT
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workouts (
        [ID] TEXT PRIMARY KEY,
        [username] TEXT,
        [frequency_per_week] INT,
        [daily_duration_minutes] INT,
        FOREIGN KEY (username) references users(username)
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workout_exercises (
        [workout_ID] TEXT,
        [exercise_ID] TEXT,
        [repetitions] INT,
        [set_number] INT,
        [duration] REAL,
        [distance] REAL,
        FOREIGN KEY (workout_ID) REFERENCES workout(ID),
        FOREIGN KEY (exercise_ID) REFERENCES exercises(ID)
    );
"""
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS goals (
        [ID] TEXT PRIMARY KEY,
        [username] TEXT,
        [goal_type] TEXT,
        [target_value] REAL,
        [current_value] REAL,
        [exercise_id] TEXT,
        [target_date] DATE,
        FOREIGN KEY (username) REFERENCES users(username)
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS workout_goals (
        [workout_ID] TEXT,
        [goal_ID] TEXT,
        FOREIGN KEY (workout_ID) REFERENCES workout(ID),
        FOREIGN KEY (goal_ID) REFERENCES goals(ID)
    );
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS weight_records (
        [ID] TEXT PRIMARY KEY,
        [username] TEXT,
        [weight] REAL,
        [date] DATE,
        FOREIGN KEY (username) references users(username)
    );
"""
)

connection.commit()

connection.close()
