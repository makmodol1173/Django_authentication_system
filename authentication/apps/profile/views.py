from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
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
            data = {'name': user[1], 'email': user[2]} 
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
        current_hashed_password = user[3] 

        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Manually verify current password by comparing hashes
            current_hashed_password_bytes = current_hashed_password.encode('utf-8') 
            userBytes = current_password.encode('utf-8')
            result = bcrypt.checkpw(userBytes, current_hashed_password_bytes) 

            if not result:
                return render(request, 'Profile.html', {'message': "Current password is incorrect.", 'user': {'name': user[1], 'email': user[2]}})
        

            if new_password != confirm_password:
                return render(request, 'Profile.html', {'message': "New passwords do not match.", 'user': {'name': user[1], 'email': user[2]}})

            # Hash the new password and update it in the database
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            update_query = "UPDATE users SET password = %s WHERE id = %s"
            cursor.execute(update_query, (hashed_password, user_id))
            db.commit()
            
            return render(request, 'Profile.html', {'message': { "update_password":"Password Update Successfully"}, 'user': {'name': user[1], 'email': user[2]}})

    except Exception as e:
        print(f"Database error: {e}")
        return redirect('/profile/')
    finally:
        if db:
            db.close()

    return redirect('/profile/')

def upload_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        auth_token = request.COOKIES.get('auth_token')

        if not auth_token:
            return redirect('login')

        # Connect to MySQL
        db = sql.connect(
            host="localhost", user="root", password="73060694moaz@", database="registration"
        )
        cursor = db.cursor()

        # Fetch the user by email (auth_token as email)
        cursor.execute("SELECT * FROM users WHERE email = %s", (auth_token,))
        user = cursor.fetchone()

        if not user:
            return redirect('login')

        user_id = user[0]  # Assuming the id is the first column

        # Handle file upload
        uploaded_file = request.FILES['profile_picture']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile_pictures'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = f'profile_pictures/{filename}'
        
        # print(f"Uploaded file: {uploaded_file.name}")
        # print(f"Saved file URL: {file_url}")
        
        # Update profile_picture column in the database
        update_query = "UPDATE users SET profile_picture = %s WHERE id = %s"
        cursor.execute(update_query, (file_url, user_id))
        # db.commit()
        # db.close()
        
        messages.success(request, "Profile picture updated successfully!")
        # return redirect('/profile/')

        cursor.execute("SELECT * FROM users WHERE email = %s", (auth_token,))
        user = cursor.fetchone()
        print(user)
        print(user[4])
        
        return render(request, 'Profile.html', {'message': { "upload_picture":"Profile picture uploaded"}, 'user': {'name': user[1], 'email': user[2], 'profile_picture':user[4]}})
        
    return render(request, 'Profile.html')

def profile_view(request):
    auth_token = request.COOKIES.get('auth_token')

    if not auth_token:
        return redirect('login')

    try:
        # Connect to MySQL database
        db = sql.connect(
            host="localhost", user="root", password="73060694moaz@", database="registration"
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (auth_token,))
        user = cursor.fetchone()

        if user:
            user_data = {
                'name': user['name'],
                'email': user['email'],
                'profile_picture': f"{settings.MEDIA_URL}{user['profile_picture']}" if user['profile_picture'] else '/static/image.png'
            }
        else:
            return redirect('login')

        db.close()
        return render(request, 'Profile.html', {'user': 'profile_picture'})

    except Exception as e:
        print(f"Error: {e}")
        return redirect('login')

