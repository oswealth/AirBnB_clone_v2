#!/usr/bin/python3
"""Starts Flask web app with specified routes and default text handling.
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hbnb_route():
    """Displays 'Hello HBNB!'"""
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return "HBNB"

@app.route('/c/<string:text>', strict_slashes=False)
def c_text(text):
    """Displays 'C' followed by the value of the text variable, with underscores replaced by spaces."""
    text = text.replace("_", " ")
    return "C %s" % text

@app.route('/python', strict_slashes=False)
@app.route('/python/<string:text>', strict_slashes=False)
def python_text(text="is cool"):
    """Displays 'Python', followed by the value of the text variable or 'is cool' if text is not provided, with underscores replaced by spaces."""
    text = text.replace("_", " ")
    return "Python %s" % text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
