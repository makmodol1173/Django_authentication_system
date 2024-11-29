from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector as sql

def add_course_view(request):
    if request.method == "POST":
        # Get the form data
        course_code = request.POST.get("course_code")
        course_title = request.POST.get("course_title")
        credit = request.POST.get("credit")
        teacher_name = request.POST.get("teacher_name")

        # Connect to the MySQL database
        try:
            database_connection = sql.connect(
                host="localhost", user="root", password="73060694moaz@", database="registration"
            )
            cursor = database_connection.cursor()

            # Check if the course code already exists
            query = "SELECT * FROM courses WHERE course_code = %s"
            cursor.execute(query, (course_code,))
            data = cursor.fetchone()

            if data:
                messages.error(request, "Course code already exists. Please use a different code.")
                return redirect("/profile")

            # Insert the course data into the database
            insert_query = """
                INSERT INTO courses (course_code, course_title, credit, teacher_name)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (course_code, course_title, credit, teacher_name))
            database_connection.commit()

            messages.success(request, "Course added successfully!")
            return redirect("/profile")  # Or redirect to a course list or another page

        except sql.Error as e:
            # Log the error and provide a message to the user
            messages.error(request, f"An error occurred while adding the course: {e}")
            return redirect("/profile")

        finally:
            cursor.close()
            database_connection.close()

    return render(request, "AddCourse.html")
