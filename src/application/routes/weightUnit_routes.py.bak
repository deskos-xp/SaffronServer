from flask import make_response,request
from flask import current_app as app
from ..models.weightUnit import db,auth,ma,WeightUnit,WeightUnitSchema
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,status_codes,ccj

@app.route("/weightUnit/delete/<weightUnit_id>",methods=["delete"])
@auth.login_required
def delete_weightUnit(weightUnit_id): 
    return delete(weightUnit_id,WeightUnit)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/weightUnit/get/<ID>",methods=["get"])
@auth.login_required
def get_weightUnit_id(ID):
    if ID == None:
        return status(WeightUnit(),status=status_codes.NO_ID_PROVIDED,msg="no weightUnit id provided!")
    weightUnit=db.session.query(WeightUnit).filter_by(id=ID).first()
    
    if weightUnit == None:
        return status(WeightUnit(),status=status_codes.INVALID_ID,msg="invalid weightUnit!")
    weightUnitSchema=WeightUnitSchema()
    return status(WeightUnit(),status=status_codes.OBJECT,object=weightUnitSchema.dump(weightUnit))


@app.route("/weightUnit/get",methods=["post"])
@auth.login_required
def get_weightUnit():
    json=request.get_json(force=True)
    json=ccj(json)
    print(json)
    assert json != None
    page=json.get('page')
    limit=json.get('limit')
    if page == None:
        page=0
    if limit == None:
        limit=10
    
    if json.get('limit') != None:
        json.__delitem__('limit')
    if json.get('page') != None:
        json.__delitem__('page')
    
    weightUnites=db.session.query(WeightUnit).filter_by(**json).limit(limit).offset(page*limit).all()
    weightUnitSchema=WeightUnitSchema()
    weightUnitesL=[weightUnitSchema.dump(i) for i in weightUnites]
    return status(WeightUnit(),status=status_codes.OBJECTS,objects=Json.dumps(weightUnitesL))

@app.route("/weightUnit/new",methods=["post"])
@auth.login_required
def add_weightUnit():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    if len(json.keys()) > 0:
        qb=db.session.query(WeightUnit).filter_by(**json).first()
        if qb != None:
            return status(qb,"old")
    weightUnit=WeightUnit(**json)
    db.session.add(weightUnit)
    db.session.commit()
    db.session.flush()
    return status(weightUnit,status=status_codes.NEW)

@app.route("/weightUnit/update/<ID>",methods=["post"])
@auth.login_required
def update_weightUnit(ID):
    assert ID != None
    weightUnit_old=db.session.query(WeightUnit).filter_by(id=ID).first()
    assert weightUnit_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in weightUnit_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in weightUnit_old.__dict__.keys()
            assert key in json.keys()
            weightUnit_old.__dict__[key]=json[key]
            flag_modified(weightUnit_old,key)
    db.session.merge(weightUnit_old)
    db.session.flush()
    db.session.commit()
    return status(weightUnit,status_codes.UPDATED) 
