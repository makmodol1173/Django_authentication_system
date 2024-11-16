# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import mysql.connector as sql


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        database_connection = sql.connect(host="localhost",user="root",password="73060694moaz@",database="registration")
        cursor=database_connection.cursor()

        query = "SELECT * FROM users WHERE email='{}' AND password ='{}'".format(email, password)
        cursor.execute(query)
        
        data = tuple(cursor.fetchall())

        if data: 
            email, password = data[0][0], data[0][1]
            if password == password:
                return redirect('/profile')

    return render(request, 'Login.html')