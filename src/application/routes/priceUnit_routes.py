from flask import make_response,request
from flask import current_app as app
from ..models.priceUnit import db,auth,ma,PriceUnit,PriceUnitSchema
import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

@app.route("/priceUnit/delete/<ID>",methods=["delete"])
@auth.login_required
def delete_priceUnit(ID):
    return delete(ID,PriceUnit)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/priceUnit/get/<ID>",methods=["get"])
@auth.login_required
def get_priceUnit_id(ID):
    if ID == None:
        return status(PriceUnit(),status=status_codes.NO_ID_PROVIDED,msg="no priceUnit id provided!")
    priceUnit=db.session.query(PriceUnit).filter_by(id=ID).first()
    if priceUnit == None:
        return status(PriceUnit(),status=status_codes.INVALID_ID,msg="invalid priceUnit!")
    priceUnitSchema=PriceUnitSchema()
    return status(PriceUnit(),status=status_codes.OBJECT,object=priceUnitSchema.dump(priceUnit))


@app.route("/priceUnit/get",methods=["post"])
@auth.login_required
def get_priceUnit():
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
    
    priceUnites=db.session.query(PriceUnit).filter_by(**json).limit(limit).offset(page*limit).all()
    priceUnitSchema=PriceUnitSchema()
    priceUnitesL=[priceUnitSchema.dump(i) for i in priceUnites]
    return status(PriceUnit(),status=status_codes.OBJECTS,objects=Json.dumps(priceUnitesL))

@app.route("/priceUnit/new",methods=["post"])
@auth.login_required
def add_priceUnit():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    if len(json.keys()) > 0:
        qb=db.session.query(PriceUnit).filter_by(**json).first()
        if qb != None:
            return status(qb,"old")

    priceUnit=PriceUnit(**json)
    db.session.add(priceUnit)
    db.session.commit()
    db.session.flush()
    return status(priceUnit,status_codes.NEW)

@app.route("/priceUnit/update/<ID>",methods=["post"])
@auth.login_required
def update_priceUnit(ID):
    assert ID != None
    priceUnit_old=db.session.query(PriceUnit).filter_by(id=ID).first()
    assert priceUnit_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in priceUnit_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in priceUnit_old.__dict__.keys()
            assert key in json.keys()
            priceUnit_old.__dict__[key]=json[key]
            flag_modified(priceUnit_old,key)
    db.session.merge(priceUnit_old)
    db.session.flush()
    db.session.commit()
    return status(priceUnit,status_codes.UPDATED) 
