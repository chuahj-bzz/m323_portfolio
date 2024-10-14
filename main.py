from flask import Flask
from book_blueprint import book_blueprint  # Import the blueprint

app = Flask(__name__)

# Register the blueprint with the app
app.register_blueprint(book_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
