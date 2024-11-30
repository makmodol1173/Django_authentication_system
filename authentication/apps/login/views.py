from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector as sql
import bcrypt

def login_view(request):
    # Check if the user is already logged in by looking for the auth_token cookie
    auth_token = request.COOKIES.get('auth_token')
    if auth_token:
        return redirect('/profile')  # If the user is logged in, redirect to profile

    # Process the POST request when the user submits the login form
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Connect to the MySQL database
            database_connection = sql.connect(
                host="localhost", user="root", password="73060694moaz@", database="registration"
            )
            cursor = database_connection.cursor()

            # Use parameterized query to avoid SQL injection
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))

            # Fetch the user data
            data = cursor.fetchone()

            if data:
                stored_password = data[3]  # Assuming the password is in the third column
                # Check if the entered password matches the hashed password stored in the DB
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    # Password matched, log the user in
                    response = redirect("/profile")
                    # Set the auth_token cookie for the user, making it secure and httpOnly
                    response.set_cookie('auth_token', email, max_age=3600, httponly=True, secure=True)
                    return response
                else:
                    messages.error(request, "Invalid password. Please try again.")
            else:
                messages.error(request, "No user found with that email address.")

            return redirect('/login')  # If login fails, stay on the login page

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('/login')

    return render(request, 'Login.html')
