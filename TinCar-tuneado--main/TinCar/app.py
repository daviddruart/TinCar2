from flask import Flask, render_template, request, redirect, url_for
from models import create_users_table, add_user, get_user_by_email
import bcrypt

app = Flask(__name__)

# Crear tabla de usuarios al iniciar
create_users_table()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')  # Convertir a bytes

        user = get_user_by_email(email)
        # Comparar password como bytes
        if user and bcrypt.checkpw(password, user['password']):
            return "Mono carechimba juas juas"
        else:
            return "Correo o contraseña incorrectos"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Guardar contraseña como bytes
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        phone = request.form['phone']
        role = request.form['role']

        if get_user_by_email(email):
            return "Este correo ya está registrado"
        
        add_user(name, email, password, phone, role)
        return redirect(url_for('login'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
