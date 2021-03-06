from .. import db,ma,auth
from passlib.apps import custom_app_context as pwd_context
from .departments import Department,DepartmentSchema
from .address import Address,AddressSchema
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

from .as_dict import AsDict
user_departments=db.Table("user_departments",
            db.Column("user_id",db.Integer,db.ForeignKey("users.id"),unique=True),
            db.Column("department_id",db.Integer,db.ForeignKey("departments.id"))
        )
user_addresses=db.Table("user_addresses",
        db.Column("user_id",db.Integer,db.ForeignKey("users.id"),unique=True),
        db.Column("address_id",db.Integer,db.ForeignKey("address.id"))
        )
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=50),unique=True)

class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Role
        fields=('name','id')
    name=ma.auto_field()


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(),db.ForeignKey("roles.id"))


class User(db.Model,AsDict,UserMixin):
    __tablename__ = 'users'
    def hash_password_auto(self):
        self.password=pwd_context.encrypt(self.password)
    def hash_password(self,password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self,password):
        i=pwd_context.verify(password,self.password)
        return i

    id = db.Column(db.Integer,primary_key=True)
    roles = db.relationship('Role',secondary='user_roles',cascade="all,delete",single_parent=True,backref='users')

    uname = db.Column(db.String(length=50))
    fname = db.Column(db.String(length=50))
    mname = db.Column(db.String(length=50))
    lname = db.Column(db.String(length=50))
    email = db.Column(db.String(length=128))
    phone = db.Column(db.String(length=15))
    carrier=db.Column(db.String(length=12))
    active= db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    region = db.Column(db.String(length=5))
    password = db.Column(db.String(length=128))
    #department_id=db.Column(db.Integer)
    departments=db.relationship("Department",backref=db.backref("users"),secondary=user_departments,cascade="all,delete",single_parent=True)
    address=db.relationship("Address",backref=db.backref("address"),secondary=user_addresses,cascade="all,delete",single_parent=True)
    
    def defaultdict(self):
        return dict(uname=str(),fname=str(),mname=str(),lname=str(),id=int(),admin=str(),password=str(),email=str(),phone=int(),active=True,departments=self.departments,carrier=self.carrier,region=self.region,address=self.address)
 
    def __repr__(self):
        return """

        User(
            uname='{0}',
            fname='{1}',
            mname='{2}',
            lname='{3}',
            admin={4},
            password='{5}',
            id={6},
            email='{7}',
            phone={8},
            carrier="9",
            active={10},
            departments={11},
            address={12}
            region="{13}",
            roles={14}
            )""".format(
            self.uname,
            self.fname,
            self.mname,
            self.lname,
            self.admin,
            self.password,
            self.id,
            self.email,
            self.phone,
            self.carrier,
            self.active,
            self.departments,
            self.address,
            self.region,
            self.roles
        )

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields=("id","uname","fname","mname","lname","admin","email","phone","active","departments","carrier","region","address","roles")
        #exclude=("password",)
    id = ma.auto_field()
    uname = ma.auto_field()
    fname = ma.auto_field()
    mname = ma.auto_field()
    lname = ma.auto_field()
    admin = ma.auto_field()
    #never transmit password
    #fixes across program, blanket
    #password = ma.auto_field()
    email=ma.auto_field()
    phone=ma.auto_field()
    carrier=ma.auto_field()
    active=ma.auto_field()
    region=ma.auto_field()
    departments=ma.List(ma.Nested(DepartmentSchema))
    address=ma.List(ma.Nested(AddressSchema))
    roles=ma.List(ma.Nested(RoleSchema))
