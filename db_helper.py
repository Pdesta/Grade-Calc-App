from db import get_connection

def get_subject_with_tests(name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM subjects WHERE name = %s", (name,))
    subject = cursor.fetchone()
    
    if subject:
        cursor.execute("SELECT * FROM tests WHERE subject_id = %s", (subject["id"],))
        tests = cursor.fetchall()
        subject["tests"] = tests
    
    cursor.close()
    conn.close()
    return subject

def get_all_subject_names():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name FROM subjects")
    names = [row["name"] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return names

def create_subject(name, weights):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO subjects (name, target) VALUES (%s, %s)", (name, 50))
    subject_id = cursor.lastrowid
    for weight in weights:
        cursor.execute("INSERT INTO tests (subject_id, weight, score) VALUES (%s, %s, %s)", (subject_id, weight, None))
    connection.commit()
    cursor.close()
    connection.close()

def reset_all_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tests")
    cursor.execute("DELETE FROM subjects")
    connection.commit()
    cursor.close()
    connection.close()

def reset_tests(subject_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tests SET score = NULL WHERE subject_id = %s", (subject_id,))
    connection.commit()
    cursor.close()
    connection.close()

def reset_chosen_test(subject_id, test_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tests SET score = NULL WHERE subject_id = %s AND id = %s", (subject_id, test_id))
    connection.commit()
    cursor.close()
    connection.close()

def update_target(subject_id, new_target):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE subjects SET target = %s WHERE id = %s", (new_target, subject_id))
    connection.commit()
    cursor.close()
    connection.close()

def update_test_score(subject_id, test_id, new_score):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tests SET score = %s WHERE subject_id = %s AND id = %s", (new_score, subject_id, test_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_subject(name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id FROM subjects WHERE name = %s", (name,))
    subject = cursor.fetchone()
    if subject:
        subject_id = subject['id']
        cursor.execute("DELETE FROM tests WHERE subject_id = %s", (subject_id,))
        cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
        connection.commit()
    cursor.close()
    connection.close()
