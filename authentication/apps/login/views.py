from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector as sql
import bcrypt

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

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
            stored_password = data[3]  # Assume the password is in the third column
            # Check if the entered password matches the hashed password stored in the DB
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # Password matched, log the user in
                response = redirect("/profile")
                response.set_cookie('auth_token', email, max_age=3600)
                return response
            else:
                messages.error(request, "Invalid password. Please try again.")
        else:
            messages.error(request, "No user found with that email address.")

        return redirect('/login')

    return render(request, 'Login.html')
