from flask import make_response,request
from flask import current_app as app
from ..models.price import db,auth,ma,Price,PriceSchema
from ..models.price import db,auth,ma,PriceUnit,PriceUnitSchema

import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

@app.route("/price/delete/<ID>",methods=["delete"])
@auth.login_required
def delete_price(ID):
    return delete(ID,Price)


@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']

@app.route("/price/get/<ID>",methods=["get"])
@auth.login_required
def get_price_id(ID):
    if ID == None:
        return status(Price(),status=status_codes.NO_ID_PROVIDED,msg="no price id provided!")
    price=db.session.query(Price).filter_by(id=ID).first()
    if price == None:
        return status(Price(),status=status_codes.INVALID_ID,msg="invalid price!")
    priceSchema=PriceSchema()
    return priceSchema.dump(price)


@app.route("/price/get",methods=["post"])
@auth.login_required
def get_price():
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
    
    pricees=db.session.query(Price).filter_by(**json).limit(limit).offset(page*limit).all()
    priceSchema=PriceSchema()
    pricees=[priceSchema.dump(i) for i in pricees]
    return status(Price(),status=status_codes.OBJECTS,objects=Json.dumps(pricees))

@app.route("/price/new",methods=["post"])
@auth.login_required
def add_price():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    '''
    if len(json.keys()) > 0:
        qb=db.session.query(Price).filter_by(**json).first()
        if qb != None:
            return status(qb,status=status_codes.OLD) 
    '''
    price=Price(**json)
    db.session.add(price)
    db.session.commit()
    db.session.flush()
    return status(price,status=status_codes.NEW) 

@app.route("/price/update/<ID>",methods=["post"])
@auth.login_required
def update_price(ID):
    assert ID != None
    price_old=db.session.query(Price).filter_by(id=ID).first()
    assert price_old != None
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    for key in price_old.defaultdict().keys():
        if key not in ["id"]:
            assert key in price_old.__dict__.keys()
            assert key in json.keys()
            price_old.__dict__[key]=json[key]
            flag_modified(price_old,key)
    db.session.merge(price_old)
    db.session.flush()
    db.session.commit()
    return status(Price(),status=status_codes.UPDATED)

@app.route("/price/update/<PRICE_ID>/add/<PRICEUNIT_ID>",methods=["get"])
@auth.login_required
def update_price_with_priceUnit_add(PRICE_ID,PRICEUNIT_ID):
    assert PRICE_ID != None
    assert PRICEUNIT_ID != None
    priceUnit=db.session.query(PriceUnit).filter_by(id=PRICEUNIT_ID).first()
    assert priceUnit != None
    price_old=db.session.query(Price).filter_by(id=PRICE_ID).first()
    assert price_old != None
    #price_old.price_unit.append(priceUnit)
    #db.session.commit()
    #return "price updated!"
    if priceUnit not in price_old.price_unit:
        price_old.price_unit.append(priceUnit)
        db.session.commit()
        return status(Price(),status=status_codes.UPDATED)
    else:
        return status(Price(),status=status_codes.NOT_UPDATED)

@app.route("/price/update/<PRICE_ID>/remove/<PRICEUNIT_ID>",methods=["get"])
@auth.login_required
def update_price_with_priceUnit_rm(PRICE_ID,PRICEUNIT_ID):
    assert PRICE_ID != None
    assert PRICEUNIT_ID != None
    priceUnit=db.session.query(PriceUnit).filter_by(id=PRICEUNIT_ID).first()
    assert priceUnit != None
    price=db.session.query(Price).filter_by(id=PRICE_ID).first()
    assert price_old != None
    price.price_unit.remove(priceUnit)
    db.session.commit()
    return status(Price(),status=status_codes.UPDATED)


