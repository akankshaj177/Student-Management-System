import sqlite3


# ---------------- DATABASE CONNECTION ----------------

def connect_database():
    return sqlite3.connect("students.db")


# ---------------- CREATE TABLE ----------------

def create_table():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------- ADD STUDENT ----------------

def add_student():
    try:
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Student Name: ")
        course = input("Enter Course: ")
        marks = float(input("Enter Marks: "))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (id, name, course, marks)
            VALUES (?, ?, ?, ?)
        """, (student_id, name, course, marks))

        connection.commit()
        connection.close()

        print("\nStudent added successfully!")

    except ValueError:
        print("\nPlease enter valid ID and marks.")

    except sqlite3.IntegrityError:
        print("\nStudent ID already exists.")


# ---------------- VIEW STUDENTS ----------------

def view_students():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    if not students:
        print("\nNo student records found.")
        return

    print("\n========== STUDENT RECORDS ==========")

    for student in students:
        print(f"""
Student ID : {student[0]}
Name       : {student[1]}
Course     : {student[2]}
Marks      : {student[3]}
--------------------------------------
""")


# ---------------- SEARCH STUDENT ----------------

def search_student():
    try:
        student_id = int(input("Enter Student ID to search: "))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        connection.close()

        if student:
            print("\n========== STUDENT FOUND ==========")
            print("Student ID :", student[0])
            print("Name       :", student[1])
            print("Course     :", student[2])
            print("Marks      :", student[3])
        else:
            print("\nStudent not found.")

    except ValueError:
        print("\nPlease enter a valid Student ID.")


# ---------------- UPDATE STUDENT ----------------

def update_student():
    try:
        student_id = int(input("Enter Student ID to update: "))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("\nStudent not found.")
            connection.close()
            return

        print("\nEnter new details:")

        name = input("Enter New Name: ")
        course = input("Enter New Course: ")
        marks = float(input("Enter New Marks: "))

        cursor.execute("""
            UPDATE students
            SET name = ?, course = ?, marks = ?
            WHERE id = ?
        """, (name, course, marks, student_id))

        connection.commit()
        connection.close()

        print("\nStudent updated successfully!")

    except ValueError:
        print("\nPlease enter valid data.")


# ---------------- DELETE STUDENT ----------------

def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("\nStudent not found.")
            connection.close()
            return

        confirmation = input(
            "Are you sure you want to delete this student? (yes/no): "
        )

        if confirmation.lower() == "yes":

            cursor.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )

            connection.commit()

            print("\nStudent deleted successfully!")

        else:
            print("\nDelete operation cancelled.")

        connection.close()

    except ValueError:
        print("\nPlease enter a valid Student ID.")


# ---------------- MAIN MENU ----------------

def main():

    create_table()

    while True:

        print("\n======================================")
        print("       STUDENT MANAGEMENT SYSTEM")
        print("======================================")

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("\nThank you for using Student Management System!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


# ---------------- PROGRAM START ----------------

if __name__ == "__main__":
    main()