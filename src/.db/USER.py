class User(user.base.Model):
    __tablename__ = 'users'
    def hash_passpword(self,password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self,password):
        return pwd_context.verify(password,self.password)

    id = user.base.Column(user.base.Integer,primary_key=True)
    uname = user.base.Column(user.base.String(length=50))
    fname = user.base.Column(user.base.String(length=50))
    mname = user.base.Column(user.base.String(length=50))
    lname = user.base.Column(user.base.String(length=50))
    role = user.base.Column(user.base.String(length=10))
    password = user.base.Column(user.base.String(length=128))
    '''
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    '''
    

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



