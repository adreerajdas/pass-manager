from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import subprocess

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ **Database Connection**
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2405",
        database="adreepass"
    )
    cursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
    exit()

# ✅ **Flask-Login Setup**
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT id, username, email FROM user WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user[0], user[1], user[2])
    return None

# ✅ **Encryption & Decryption Using Java**
def encrypt_password(password):
    try:
        result = subprocess.run(
            ["java", "-cp", "passwordencryptor.jar", "PasswordEncryptor", "encrypt", password], 
            capture_output=True, text=True
        )
        return result.stdout.strip().split(":")[-1].strip()
    except Exception as e:
        print(f"Encryption Error: {e}")
        return None

def decrypt_password(encrypted_password):
    try:
        result = subprocess.run(
            ["java", "-cp", "passwordencryptor.jar", "PasswordEncryptor", "decrypt", encrypted_password], 
            capture_output=True, text=True
        )
        return result.stdout.strip().split(":")[-1].strip()
    except Exception as e:
        print(f"Decryption Error: {e}")
        return None

# ✅ **Routes**
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = encrypt_password(request.form["password"])

        if not password:
            flash("Encryption failed. Please try again.", "danger")
            return redirect(url_for("register"))

        try:
            cursor.execute("INSERT INTO user (username, email, password_hash) VALUES (%s, %s, %s)", 
                           (username, email, password))
            db.commit()
            flash("Registration Successful! Please login.", "success")
            return redirect(url_for("login"))
        except mysql.connector.Error as e:
            flash(f"Error: {e}", "danger")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT id, username, password_hash FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and decrypt_password(user[2]) == password:
            user_obj = User(user[0], user[1], email)
            login_user(user_obj)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        title = request.form["title"]
        stored_password = encrypt_password(request.form["stored_password"])
        note = request.form["note"]

        if not stored_password:
            flash("Encryption failed. Please try again.", "danger")
            return redirect(url_for("dashboard"))

        cursor.execute("INSERT INTO user_data (user_id, title, stored_password, note) VALUES (%s, %s, %s, %s)",
                       (current_user.id, title, stored_password, note))
        db.commit()
        flash("Password & Note Saved!", "success")

    cursor.execute("SELECT id, title, stored_password, note FROM user_data WHERE user_id = %s", (current_user.id,))
    saved_data = cursor.fetchall()
    
    decrypted_data = [(entry[0], entry[1], decrypt_password(entry[2]), entry[3]) for entry in saved_data]

    return render_template("dashboard.html", username=current_user.username, saved_data=decrypted_data)

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        cursor.execute("SELECT id, username FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Password reset instructions sent to your email.", "info")
            # Implement email functionality here
        else:
            flash("Email not found!", "danger")

    return render_template("forgot_password.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
