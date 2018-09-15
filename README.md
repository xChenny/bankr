# Bankr

## Setting up Flask backend server

Install MongoDB and Python3 for your computer.

Create a virtualenv: virtualenv ENV

Activate your virtual environment: source ENV/bin/activate

Install backend requirements: pip install -e .

Export the FLASK_APP environment variable: export FLASK_APP=backend

Create your MongoDB database directory: mkdir db

Run MongoDB with this directory: mongod --dbpath db --bind-ip 127.0.0.1

Run the Flask server: flask run
