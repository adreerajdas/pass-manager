# Adree Password Manager

## Setup Instructions
1. Install dependencies:
   ```sh
   pip install flask flask-mysql flask-bcrypt flask-login
   ```

2. Create the database:
   ```sh
   mysql -u root -p < database.sql
   ```

3. Compile the Java encryption file:
   ```sh
   javac java/PasswordEncryptor.java
   jar cf passwordencryptor.jar -C java PasswordEncryptor.class
   ```

4. Run the Flask application:
   ```sh
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.
