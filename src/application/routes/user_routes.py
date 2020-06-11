from flask import request,make_response 
from flask import current_app as app
from ..models.user import db,User,UserSchema,auth,Role
from ..models.departments import Department
from ..models.address import Address
import os
import json as Json
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
#from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from ..decor import roles_required
@app.route("/user/delete/<user_id>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_user(user_id): 
    return delete(user_id,User)

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']


@app.route("/user/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=["admin","user"])
def get_user_by_id(ID):
    USER=db.session.query(User).filter_by(id=ID).first()
    USER.password="xxxxx"
    userSchema = UserSchema()
    return status(User(),status=status_codes.OBJECT,object=userSchema.dump(USER))

@app.route("/user/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def search_user():
    print(request.view_args)
    json=request.get_json(force=True)
    json=ccj(json)
    page=json.get("page")
    limit=json.get("limit")
    if page != None:
        json.__delitem__("page")
    if limit != None:
        json.__delitem__("limit")

    if page == None:
        page=0
    if limit == None:
        limit=10
    userSchema = UserSchema()
    USERS=db.session.query(User).filter_by(**json).limit(limit).offset(limit*page).all()
    users_j=[userSchema.dump(i) for i in USERS]
    #do not transmit password hashes
    for u in users_j:
        u['password']="xxxxx"
    return status(User(),status=status_codes.OBJECTS,objects=Json.dumps(users_j))

@app.route("/user/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def alter_user(ID):
    json=request.get_json(force=True)
    json=ccj(json)
    #assert ID == request.view_args['ID']
    #print(ID)
    #getuser
    admin=db.session.query(User).filter_by(uname=auth.username()).first()
    assert admin != None
    assert admin.admin != False
    USER=db.session.query(User).filter_by(id=ID).first()        
    assert USER != None
    #update fields
    for key in USER.defaultdict().keys():
        if json.get(key) != None:
            field=json.get(key)
            if field != USER:
                USER.__dict__[key]=field
                #flag modified fields
                flag_modified(USER,key)
    #ensure password is hashed
    USER.hash_password_auto()
    #commit the data
    db.session.merge(USER)
    db.session.flush()
    db.session.commit()  
    return status(User(),status=status_codes.UPDATED)
#need to add department route
@app.route("/user/update/<ID>/add/department/<DEPARTMENT_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def add_department_to_user(ID,DEPARTMENT_ID):
    assert ID != None
    assert DEPARTMENT_ID != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    department=db.session.query(Department).filter_by(id=DEPARTMENT_ID).first()
    assert department != None
    if department in user.departments:
        return status(User(),status=status_codes.NOT_UPDATED)
    user.departments.append(department)
    flag_modified(user,"departments")
    db.session.flush()
    db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)

@app.route("/user/update/<ID>/add/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def add_address_to_user(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS_ID != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    if address in user.address:
        return status(User(),status=status_codes.NOT_UPDATED)
    user.address.append(address)
    flag_modified(user,"address")
    db.session.flush()
    db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)

@app.route("/user/update/<ID>/remove/address/<ADDRESS_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def remove_address_from_user(ID,ADDRESS_ID):
    assert ID != None
    assert ADDRESS != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    address=db.session.query(Address).filter_by(id=ADDRESS_ID).first()
    assert address != None
    assert address in user.addresss
    user.address.remove(address)
    flag_modified(user,"address")
    db.session.flush()
    db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)


if os.environ['NEED_ADMIN'] == "True":
    @app.route("/admin/new",methods=["get"])
    def new_admin():    
        if os.environ['NEED_ADMIN'] == "True":
            result=default_user()
            if result[1] == 200:
                return status(User(),status=status_codes.NEW,msg="admin created! please set need_admin to false and restart server!")
            else:
                return status(User(),status=status_codes.OLD,msg=result[0])

@app.route("/user/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def new_user():
    json=request.get_json(force=True)
    json=ccj(json)
    roleName=None
    if 'role' in json.keys():
        roleName=json.get('role')
    elif 'roles' in json.keys():
        roleName=json.get("roles")
    if 'role' in json.keys():
        json.__delitem__('role')
    elif 'roles' in json.keys():
        json.__delitem__('roles')
    
    print(json) 
    if db.session.query(User).filter_by(uname=auth.username()).first().active:
        print(json)
        user=User(**json)

        user.hash_password(json['password'])
        json.__delitem__('password')
        exists=db.session.query(User).filter_by(**json).first()
        print(exists)
        if exists != None:
            return status(exists,status=status_codes.OLD) 
        if roleName != None:
            role=db.session.query(Role).filter_by(name=roleName).first()
            if not role:
                user.roles.append(Role(name=roleName))
            else:
                user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        return status(db.session.query(User).filter_by(uname=json['uname']).first(),status=status_codes.NEW)
        #return status(user,"new")
    else:
        return status(User(),status=status_codes.INVALID_ID)


def query_user(uname="admin"):
    user = session.query(User).filter_by(uname="admin").first()
    print(user)
    return user;

def default_user():
    default_user = User(uname="admin",fname="first_name",mname="middle_name",lname="last_name",admin=True,email="admin@localhost",phone=1000000000,active=True)
    user=db.session.query(User).filter_by(uname=default_user.uname).first()
    if user:
        return "user exists",400
    default_user.hash_password("avalon")
    role=db.session.query(Role).filter_by(name='admin').first()
    if not role:
        role=Role(name='admin')
    default_user.roles.append(role)
    db.session.add(default_user)
    db.session.commit()
    return "user created",200


@app.route("/user/update/<ID>/add/roles/<ROLE_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def add_roles_to_user(ID,ROLE_ID):
    assert ID != None
    assert ROLE_ID != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    roles=db.session.query(Role).filter_by(id=ROLE_ID).first()
    assert roles != None
    if roles in user.roles:
        return status(User(),status=status_codes.NOT_UPDATED)
    user.roles.append(roles)
    flag_modified(user,"roles")
    db.session.flush()
    db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)

@app.route("/user/update/<ID>/remove/department/<DEPARTMENT_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def remove_department_from_user(ID,DEPARTMENT_ID):
    assert ID != None
    assert DEPARTMENT_ID != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    department=db.session.query(Department).filter_by(id=DEPARTMENT_ID).first()
    assert department != None
    assert department in user.departments
    user.departments.remove(department)
    #flag_modified(user,"departments")
    #db.session.flush()
    #db.session.merge(user)
    print(user.departments)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)


@app.route("/user/update/<ID>/remove/roles/<ROLE_ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin'])
def remove_roles_from_user(ID,ROLE_ID):
    assert ID != None
    assert ROLE_ID != None
    user=db.session.query(User).filter_by(id=ID).first()
    assert user != None
    roles=db.session.query(Role).filter_by(id=ROLE_ID).first()
    assert roles != None
    assert roles in user.roles
    user.roles.remove(roles)
    #print(user.roles)
    #flag_modified(user,"roles")
    #db.session.flush()
    #db.session.merge(user)
    db.session.flush()
    db.session.commit()
    return status(User(),status=status_codes.UPDATED)


