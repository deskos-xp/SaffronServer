from flask import request,make_response
from flask import current_app as app
from ..models.departments import db,auth,Department,DepartmentSchema 
import os
import json as Json
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes
from ..decor import roles_required
from ..messages import messages

@app.route("/department/delete/<ID>",methods=["delete"])
@auth.login_required
@roles_required(roles=['admin'])
def delete_department(ID):
    if not ID:
        return messages.NO_ID.value
    return delete(ID,Department)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/department/new",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def new_department():
    json=request.get_json(force=True)
    json=ccj(json)
    #assert json != None
    if not json:
        return messages.NO_JSON.value
    if len(json.keys()) > 0:
        exists=db.session.query(Department).filter_by(**json).first()
        if exists != None:
            return status(exists,status=status_codes.OLD)
    department=Department(**json) 
    db.session.add(department)
    db.session.commit()
    db.session.flush()
    return status(department,status=status_codes.NEW)        

@app.route("/department/get/<ID>",methods=["get"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_department_id(ID):
    department=db.session.query(Department).filter_by(id=ID).first() 
    if department == None:
        return status(Department(),status=status_codes.INVALID_ID,msg="no such department!")
    departmentSchema=DepartmentSchema()
    return status(Department(),status=status_codes.OBJECT,object=departmentSchema.dump(department))

@app.route("/department/get",methods=["post"])
@auth.login_required
@roles_required(roles=['admin','user'])
def get_department():
    json=request.get_json(force=True)
    json=ccj(json)
    page=json.get("page")
    limit=json.get("limit")
    departmentSchema=DepartmentSchema()
    if page == None:
        page=0
    if limit == None:
        limit=10
    if ( limit != None ) or ( page != None ) or ( page != None and limit != None):
        for i in ["page","limit"]:
            if i in json.keys():
                json.__delitem__(i)
    departments=db.session.query(Department).filter_by(**json).limit(limit).offset(page*limit).all()

    results=[departmentSchema.dump(i) for i in departments]
    if departments == []:
        return status(Department(),status=status_codes.INVALID_ID,msg="no such department!")
    return status(Department(),status=status_codes.OBJECTS,objects=Json.dumps(results))

#edit department goes here
@app.route("/department/update/<ID>",methods=["post"])
@auth.login_required
@roles_required(roles=['admin'])
def update_department(ID):
    if ID == None:
        return status(Department(),status=status_codes.NO_ID_PROVIDED,msg="department was not provided!")
    department=db.session.query(Department).filter_by(id=ID).first()
    if department == None:
        return status(Department(),status=status_codes.INVALID_ID,msg="department was not found!")
    json=request.get_json(force=True)
    json=ccj(json)
    if json == None:
        return status(Department(),status=status_codes.REQURIED_JSON_NOT_PROVIDED,msg="department json was not provided!")
    for key in department.defaultdict().keys():
        if key in department.__dict__.keys():
            if key in json.keys():
                if json[key] != department.__dict__[key]:
                    department.__dict__[key]=json[key]
                    flag_modified(department,key)
    db.session.flush()
    db.session.merge(department)
    db.session.commit()
    return status(department,status=status_codes.UPDATED)
