from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.urls import reverse
import mysql.connector as sql

def profile(request):
    # Check for authToken in cookies
    auth_token = request.COOKIES.get('auth_token')

    if not auth_token:
        # If no authToken cookie is found, redirect to login page
        return redirect('login')
    try:
        # Connect to the MySQL database
        database_connection = sql.connect(
            host="localhost", user="root", password="73060694moaz@", database="registration"
        )
        cursor = database_connection.cursor()
        
        # Check if the authToken is valid by querying the User table
        query = "SELECT * FROM users WHERE email = %s"
        # Query to find the user by auth_token
        cursor.execute(query, (auth_token,))
        user = cursor.fetchone()
        data =  {
                'name': user[1],  # Assuming name is the second column
                'email': user[2],  # Assuming email is the third column
                }
    except User.DoesNotExist:
        # If no user matches the authToken, redirect to login page
        return redirect('login')

    # If valid, render the profile page
    return render(request, 'Profile.html', {'user': data})
 
def logout(request):
    response = redirect('login')  # Replace 'login' with the name of your login URL
    response.delete_cookie('auth_token')  # Remove the auth_token cookie
    return response