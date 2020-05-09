from flask_sqlalchemy import SQLAlchemy as db
from sqlalchemy.ext.declarative import declarative_base
from passlib.apps import  custom_app_context as pwd_context
from flask_marshmallow import Marshmallow
from flask import Flask
import USER

engine = Flask(__name__)
engine.config['SQLALCHEMY_DATABASE_URI']="mysql://carl:times will change@localhost"
engine.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
base = db(engine)
base.engine.execute("create database if not exists safeway")
base.engine.execute("use safeway")

ma=Marshmallow(engine)


class User(base.Model):
    __tablename__ = 'users'
    def hash_passpword(self,password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self,password):
        return pwd_context.verify(password,self.password)

    id = base.Column(base.Integer,primary_key=True)
    uname = base.Column(base.String(length=50))
    fname = base.Column(base.String(length=50))
    mname = base.Column(base.String(length=50))
    lname = base.Column(base.String(length=50))
    role = base.Column(base.String(length=10))
    password = base.Column(base.String(length=128))
    
    def __repr__(self):
        return "<User(uname='{0}',fname='{1}',mname='{2}',lname='{3}',role='{4}',password='{6}',id={5}".format(
            self.uname,
            self.fname,
            self.mname,
            self.lname,
            self.role,
            self.id,
            self.password
        )
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    id = ma.auto_field()
    uname = ma.auto_field()
    fname = ma.auto_field()
    mname = ma.auto_field()
    lname = ma.auto_field()
    role = ma.auto_field()
    password = ma.auto_field()


class Setup(object):
    def __init__(self):
        self.engine=base
        self.__flask__=engine
        self.engine.create_all()
        self.session=self.engine.session
        print(__name__)
        if __name__ == "__main__":
            if self.query_user() == None:
                self.default_user()
                self.query_user()
            else:
                raise Exception("there is already an user with that name!",self.query_user())

    def query_user(self,uname="admin"):
        user = self.session.query(User).filter_by(uname="admin").first()
        print(user)
        return user;

    def default_user(self):
        default_user = User(uname="admin",fname="admin",mname="admin",lname="admin",role="admin")
        default_user.hash_passpword("avalon")
        self.session.add(default_user)
        self.session.commit()


if __name__ == "__main__":
    Setup()
