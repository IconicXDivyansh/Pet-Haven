import os


class Config:
    SECRET_KEY = 'supersecretkey'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the project folder
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
