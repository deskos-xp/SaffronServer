from flask import request,make_response 
from flask import current_app as app
from ..models.user import db,auth,Role,RoleSchema,User
from ..models.departments import Department
from ..models.address import Address
import os
import json as Json
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..decor import roles_required
from ..messages import messages

@app.route("/roles/delete/<role_id>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_role(role_id): 
    if not role_id:
        return messages.NO_ROLE_ID.value
    return delete(role_id,Role)

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/roles/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=["admin","role"])
def get_role_by_id(ID):
    if not ID:
        return messages.NO_ID.value
    ROLE=db.session.query(Role).filter_by(id=ID).first()
    ROLE.password="xxxxx"
    roleSchema = RoleSchema()
    return status(Role(),status=status_codes.OBJECT,object=roleSchema.dump(ROLE))

@app.route("/roles/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','role'])
def search_role():
    print(request.view_args)
    json=request.get_json(force=True)
    if not json:
        return messages.NO_JSON.value
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
    roleSchema = RoleSchema()
    ROLES=db.session.query(Role).filter_by(**json).limit(limit).offset(limit*page).all()
    roles_j=[roleSchema.dump(i) for i in ROLES]
    #do not transmit password hashes
    return status(Role(),status=status_codes.OBJECTS,objects=Json.dumps(roles_j))

@app.route("/roles/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def alter_role(ID):
    json=request.get_json(force=True)
    if not json:
        return messages.NO_JSON.value
    json=ccj(json)
    #assert ID == request.view_args['ID']
    #print(ID)
    #getrole
    admin=db.session.query(Role).filter_by(uname=auth.rolename()).first()
    #assert admin != None
    if not admin:
        return messages.ENTITY_DOES_NOT_EXIST_ROLE.value
    #assert admin.admin != False
    if not admin.admin:
        return messages.NOT_ADMIN.value

    ROLE=db.session.query(Role).filter_by(id=ID).first()        
    #assert ROLE != None
    if not ROLE:
        return messages.ENTITY_DOES_NOT_EXIST_ROLE.value
    #update fields
    for key in ROLE.defaultdict().keys():
        if json.get(key) != None:
            field=json.get(key)
            if field != ROLE:
                ROLE.__dict__[key]=field
                #flag modified fields
                flag_modified(ROLE,key)
    #ensure password is hashed
    ROLE.hash_password_auto()
    #commit the data
    db.session.merge(ROLE)
    db.session.flush()
    db.session.commit()  
    return status(Role(),status=status_codes.UPDATED)

@app.route("/roles/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def new_role():
    json=request.get_json(force=True)
    if not json:
        return messages.NO_JSON.value
    json=ccj(json)
    print(json) 
    if db.session.query(User).filter_by(uname=auth.username()).first().active:
        role=Role(**json)

        exists=db.session.query(Role).filter_by(**json).first()
        print(exists)
        if exists != None:
            return status(exists,status=status_codes.OLD) 
        db.session.add(role)
        db.session.commit()
        db.session.flush()
        return status(role,status=status_codes.NEW)
        #return status(user,"new")
    else:
        return status(User(),status=status_codes.INVALID_ID)



