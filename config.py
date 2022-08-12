import os 

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "ahh-ahh-ahh-you-didn't-say-the-magic-word"
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')