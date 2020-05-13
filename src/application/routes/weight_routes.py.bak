from flask import make_response,request
from flask import current_app as app
from ..models.weight import db,auth,ma,Weight,WeightSchema
from ..models.weight import db,auth,ma,WeightUnit,WeightUnitSchema

import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

@app.route("/weight/delete/<weight_id>",methods=["delete"])
@auth.login_required
def delete_weight(weight_id): 
    return delete(weight_id,Weight)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/weight/get/<ID>",methods=["get"])
@auth.login_required
def get_weight_id(ID):
    if ID == None:
        return status(Weight(),status=status_codes.NO_ID_PROVIDED,msg="no weight id provided!")
    weight=db.session.query(Weight).filter_by(id=ID).first()
    if weight == None:
        return status(Weight(),status=status_codes.INVALID_ID,msg="invalid weight!")
    weightSchema=WeightSchema()
    return status(Weight(),status=status_codes.OBJECT,object=weightSchema.dump(weight))


@app.route("/weight/get",methods=["post"])
@auth.login_required
def get_weight():
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
    
    weightes=db.session.query(Weight).filter_by(**json).limit(limit).offset(page*limit).all()
    weightSchema=WeightSchema()
    weightes=[weightSchema.dump(i) for i in weightes]
    return status(Weight(),status=status_codes.OBJECTS,objects=Json.dumps(weightes))

@app.route("/weight/new",methods=["post"])
@auth.login_required
def add_weight():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    '''
    if len(json.keys()) > 0:
        qb=db.session.query(Weight).filter_by(**json).first()
        if qb != None:
            return status(qb,"old")
    '''
    weight=Weight(**json)
    db.session.add(weight)
    db.session.commit()
    db.session.flush()
    return status(weight,status=status_codes.NEW)

@app.route("/weight/update/<WEIGHT_ID>/add/<WEIGHTUNIT_ID>",methods=["get"])
@auth.login_required
def update_weight_with_weightUnit_add(WEIGHT_ID,WEIGHTUNIT_ID):
    assert WEIGHT_ID != None
    assert WEIGHTUNIT_ID != None
    weightUnit=db.session.query(WeightUnit).filter_by(id=WEIGHTUNIT_ID).first()
    assert weightUnit != None
    weight_old=db.session.query(Weight).filter_by(id=WEIGHT_ID).first()
    assert weight_old != None
    if weightUnit not in weight_old.weight_unit:
        weight_old.weight_unit.append(weightUnit)
        db.session.commit()
        return status(weight_old,status=status_codes.UPDATED) 
    else:
        return status(weight_old,status=status_codes.NOT_UPDATED)

@app.route("/weight/update/<WEIGHT_ID>/remove/<WEIGHTUNIT_ID>",methods=["get"])
@auth.login_required
def update_weight_with_weightUnit_rm(WEIGHT_ID,WEIGHTUNIT_ID):
    assert WEIGHT_ID != None
    assert WEIGHTUNIT_ID != None
    weightUnit=db.session.query(WeightUnit).filter_by(id=WEIGHTUNIT_ID).first()
    assert weightUnit != None
    weight_old=db.session.query(Weight).filter_by(id=WEIGHT_ID).first()
    assert weight_old != None
    weight_old.weight_unit.remove(weightUnit)
    db.session.commit()
    return status(weight_old,status=status_codes.UPDATED)


@app.route("/weight/update/<ID>",methods=["post"])
@auth.login_required
def update_weight(ID):
    assert ID != None
    weight_old=db.session.query(Weight).filter_by(id=ID).first()
    assert weight_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in weight_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in weight_old.__dict__.keys()
            assert key in json.keys()
            weight_old.__dict__[key]=json[key]
            flag_modified(weight_old,key)
    db.session.merge(weight_old)
    db.session.flush()
    db.session.commit()
    return status(weight_old,status=status_codes.UPDATED)
