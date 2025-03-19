from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text for raw SQL queries

app = Flask(__name__)

# Database configuration
#Format - mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database-name>
DB_URI = "mysql+mysqlconnector://avnadmin:AVNS_1IFH9IcBTp6gE8enJ0g@mysql-252ca5de-mysqlpassword.h.aivencloud.com:26889/adreepass"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

@app.route('/')
def home():
    try:
        db.session.execute(text("SELECT 1"))  # ✅ Use text() for raw SQL
        return "✅ Database connection established!"
    except Exception as e:
        return f"❌ Database connection failed: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
