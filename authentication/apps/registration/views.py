# views.py (Registration View)
from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector as sql
import bcrypt

def registration_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Hash the password before saving it to the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Connect to the MySQL database
        database_connection = sql.connect(
            host="localhost", user="root", password="73060694moaz@", database="registration"
        )
        cursor = database_connection.cursor()

        # Check if the email is already registered
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        data = cursor.fetchone()

        if data:
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect("/register")

        try:
            # Insert the user data into the database with the hashed password
            insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, email, hashed_password))
            database_connection.commit()

            # Set a cookie for the registered email (optional)
            response = redirect('/login')
            response.set_cookie('auth_token', email, max_age=3600)

            return response

        except sql.IntegrityError:
            messages.error(request, "An error occurred while registering. Please try again.")
            return redirect("/register")

        finally:
            cursor.close()
            database_connection.close()

    return render(request, "Registration.html")
