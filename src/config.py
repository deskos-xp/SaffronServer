from os import environ
from dotenv import load_dotenv
load_dotenv()

class Config:
    def __init__(self):
        
        print(self.SQLALCHEMY_DATABASE_URI)
    TESTING=environ["TESTING"]
    FLASK_DEBUG=environ["FLASK_DEBUG"]
    SECRET_KEY=environ["SECRET_KEY"]

    SQLALCHEMY_DATABASE_URI=environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS=environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
    UPLOAD_FOLDER=environ["UPLOAD_FOLDER"]
    MAX_CONTENT_LENGTH=int(environ["MAX_CONTENT_LENGTH"])
    MESSAGING_PASSWORD=environ['MESSAGING_PASSWORD']
    MESSAGING_EMAIL=environ['MESSAGING_EMAIL']
    MESSAGING_CARRIER_GATEWAY=environ['MESSAGING_CARRIER_GATEWAY']
