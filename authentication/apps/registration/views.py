from django.shortcuts import render, redirect
import mysql.connector as sql

name = ''
mail = ''
password = ''

def signaction(request):
    global name, mail, password

    if request.method == 'POST':
        # Establish the database connection
        m = sql.connect(host="localhost", user="root", password="73060694moaz@", database="registration")
        cursor = m.cursor()

        # Capture form data
        d = request.POST
        for key, value in d.items():
            if key == "name":
                name = value
            if key == "email":
                mail = value
            if key == "password":
                password = value

        # Insert user into the database
        c = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(c, (name, mail, password))  
        m.commit()
        
        return redirect('/login')

    return render(request, "Registration.html")
