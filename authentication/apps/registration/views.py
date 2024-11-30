from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector as sql
import bcrypt

def registration_view(request):
    # Check if the user is already logged in by looking for the auth_token cookie
    auth_token = request.COOKIES.get('auth_token')
    if auth_token:
        return redirect('/profile')  # Redirect to profile if already logged in

    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validate the input (optional, for security and user experience)
        if not name or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("/register")

        # Hash the password before saving it to the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
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

            # Insert the user data into the database with the hashed password
            insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (name, email, hashed_password))
            database_connection.commit()

            # Set a cookie for the registered email (optional)
            response = redirect('/login')
            response.set_cookie('auth_token', email, max_age=3600, httponly=True, secure=True)

            messages.success(request, "Registration successful! You can now log in.")
            return response

        except sql.IntegrityError as e:
            messages.error(request, f"An error occurred: {str(e)}. Please try again.")
            return redirect("/register")

        finally:
            cursor.close()
            database_connection.close()

    return render(request, "Registration.html")
