import sqlite3
import uuid

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

cursor.executemany(
    """
    INSERT INTO exercises (ID, name, description, instructions, target_muscles) 
    VALUES (?, ?, ?, ?, ?);
    """,
    [
        (str(uuid.uuid4()), "Push-Up", "A bodyweight exercise that targets the chest, shoulders, and triceps.",
         "Keep your body straight, lower yourself until your chest almost touches the ground, then push back up.",
         "Chest, Triceps, Shoulders, Core"),

        (str(uuid.uuid4()), "Squat", "A lower-body strength exercise.",
         "Stand with feet shoulder-width apart, lower hips down, and return to standing.",
         "Quadriceps, Hamstrings, Glutes"),

        (str(uuid.uuid4()), "Deadlift", "A full-body strength exercise using a barbell.",
         "Hinge at hips, grip the bar, and lift it while keeping the back straight.",
         "Hamstrings, Glutes, Lower Back, Traps"),

        (str(uuid.uuid4()), "Pull-Up", "A bodyweight exercise that builds upper body strength.",
         "Grip the bar with palms facing away and pull yourself up until the chin is above the bar.",
         "Back, Biceps, Shoulders"),

        (str(uuid.uuid4()), "Lunges", "A unilateral leg exercise.",
         "Step forward with one leg, lower hips until both knees form 90-degree angles, then push back up.",
         "Quadriceps, Hamstrings, Glutes"),

        (str(uuid.uuid4()), "Plank", "An isometric core exercise.",
         "Hold a straight body position on forearms and toes, keeping the core tight.",
         "Core, Shoulders, Back"),

        (str(uuid.uuid4()), "Bench Press", "A strength exercise using a barbell or dumbbells.",
         "Lower the weight to the chest and push it back up while lying on a bench.",
         "Chest, Triceps, Shoulders"),

        (str(uuid.uuid4()), "Bent-Over Row", "A strength exercise for the back.",
         "Bend at the hips, pull a barbell or dumbbells toward the torso, and lower it slowly.",
         "Back, Biceps, Rear Delts"),

        (str(uuid.uuid4()), "Bicep Curl", "An isolation exercise for the biceps.",
         "Curl dumbbells or a barbell toward the shoulders and lower them back down.",
         "Biceps"),

        (str(uuid.uuid4()), "Triceps Dips", "A bodyweight exercise for the triceps.",
         "Lower your body by bending elbows and then push back up while gripping parallel bars.",
         "Triceps, Shoulders, Chest"),

        (str(uuid.uuid4()), "Leg Press", "A machine-based lower-body exercise.",
         "Push a weighted platform away from the body using the legs.",
         "Quadriceps, Hamstrings, Glutes"),

        (str(uuid.uuid4()), "Shoulder Press", "A strength exercise for the shoulders.",
         "Press dumbbells or a barbell overhead and return to shoulder level.",
         "Shoulders, Triceps"),

        (str(uuid.uuid4()), "Calf Raise", "An isolation exercise for the calves.",
         "Rise onto the balls of your feet and lower back down.",
         "Calves"),

        (str(uuid.uuid4()), "Russian Twists", "A rotational core exercise.",
         "Sit with knees bent, twist the torso side to side while holding a weight.",
         "Core, Obliques"),

        (str(uuid.uuid4()), "Lat Pulldown", "A machine-based exercise for the back.",
         "Pull a weighted bar down toward the chest while seated.",
         "Back, Biceps"),

        (str(uuid.uuid4()), "Step-Ups", "A lower-body strength and stability exercise.",
         "Step onto a raised platform with one foot, drive through the heel, and stand up.",
         "Quadriceps, Glutes, Hamstrings"),

        (str(uuid.uuid4()), "Hip Thrust", "A glute-focused strength exercise.",
         "Push the hips upward while lying back against a bench with a barbell over the hips.",
         "Glutes, Hamstrings"),

        (str(uuid.uuid4()), "Seated Row", "A back-focused machine exercise.",
         "Pull a cable handle toward the torso while seated.",
         "Back, Biceps"),

        (str(uuid.uuid4()), "Burpees", "A full-body explosive movement.",
         "Perform a squat, jump back into a push-up position, do a push-up, return to squat, and jump up.",
         "Full Body, Core, Legs, Shoulders"),

        (str(uuid.uuid4()), "Jump Rope", "A cardio and coordination exercise.",
         "Jump over a rope continuously while keeping a steady rhythm.",
         "Full Body, Cardio, Calves"),
    ]
)

connection.commit()

connection.close()
