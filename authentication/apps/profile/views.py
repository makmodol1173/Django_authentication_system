from django.shortcuts import render, redirect
import mysql.connector as sql
import bcrypt
from django.contrib import messages

def profile(request):
    auth_token = request.COOKIES.get('auth_token')

    if not auth_token:
        return redirect('login')

    try:
        # Connect to MySQL database
        database_connection = sql.connect(
            host="localhost", user="root", password="73060694moaz@", database="registration"
        )
        cursor = database_connection.cursor()
        
        # Query to get user by auth_token
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (auth_token,))
        user = cursor.fetchone()
        if user:
            data = {'name': user[1], 'email': user[2]}  # Assuming name is the second column and email is the third column
        else:
            return redirect('login')
    except Exception as e:
        print(f"Error: {e}")
        return redirect('login')

    return render(request, 'Profile.html', {'user': data})

def logout(request):
    response = redirect('login')
    response.delete_cookie('auth_token')
    return response

def change_password(request):
    auth_token = request.COOKIES.get('auth_token')
    if not auth_token:
        return redirect('login')

    db = None
    try:
        db = sql.connect(host="localhost", user="root", password="73060694moaz@", database="registration")
        cursor = db.cursor()

        # Query to get user data by auth_token
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (auth_token,))
        user = cursor.fetchone()

        if not user:
            return redirect('login')

        user_id = user[0]
        current_hashed_password = user[3]  # Assuming password is stored in the 4th column

        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Manually verify current password by comparing hashes

            current_hashed_password_bytes = current_hashed_password.encode('utf-8')  # Convert string to bytes
            userBytes = current_password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, current_hashed_password_bytes)  # Pass bytes
            # if result:
            #     print("Password is correct!")
            # else:
            #     print("Incorrect password.")
                
            if not result:
                print("Hello")
                return render(request, 'Profile.html', {'message': "Current password is incorrect.", 'user': {'name': user[1], 'email': user[2]}})
        

            if new_password != confirm_password:
                return render(request, 'Profile.html', {'message': "New passwords do not match.", 'user': {'name': user[1], 'email': user[2]}})

            # Hash the new password and update it in the database
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_query = "UPDATE users SET password = %s WHERE id = %s"
            cursor.execute(update_query, (hashed_password, user_id))
            db.commit()
            return render(request, 'Profile.html', {'message': "Password updated successfully.", 'user': {'name': user[1], 'email': user[2]}})

    except Exception as e:
        print(f"Database error: {e}")
        return redirect('/profile/')
    finally:
        if db:
            db.close()

    return redirect('/profile/')
