from flask import make_response,request
from flask import current_app as app

from ..models.ledger import db,auth,ma,Ledger,LedgerSchema
from ..models.user import User,UserSchema
from ..models.productCount import ProductCount,ProductCountSchema

import json as Json
import os
from sqlalchemy.orm.attributes import flag_modified
from . import verify
from .. import delete,status,ccj,status_codes

from datetime import datetime

@auth.verify_password
def v(username,password):
    a=verify.verify_password(username,password)
    return a['authorized']


@app.route("/ledger/new",methods=["post"])
@auth.login_required
def new_ledger():
        json=request.get_json(force=True)
        json=ccj(json)
        assert json != None
        if len(json.keys()) > 0:
            exists=db.session.query(Ledger).filter_by(**json).first()
            if exists != None:
                return status(exists,status=status_codes.OLD)        
        ledger=Ledger(**json)
        ledger.timestamp=datetime.now()  
        db.session.add(ledger)
        db.session.flush()
        db.session.commit()
        return status(ledger,status=status_codes.NEW) 
        '''
        return """
ledger created!
ToDos:
    /ledger/update/{0}/add/user/<user_id>
    /ledger/update/{0}/add/product/<product_id>
    /ledger/update/{0}/timestamp
""".format(ledger.id)
        '''
@app.route("/ledger/get/<ledger_id>",methods=["GET"])
@auth.login_required
def get_ledger_id(ledger_id):
    assert ledger_id != None
    ledger=db.session.query(Ledger).filter_by(id=ledger_id).first()
    if ledger == None:
        return status(Ledger(),status=status_codes.INVALID_ID,msg="no such ledger")
    ledgerSchema = LedgerSchema()
    return status(Ledger(),status=status_codes.OBJECT,object=ledgerSchema.dump(ledger))

@app.route("/ledger/get",methods=["post"])
@auth.login_required
def get_ledgers():
    json=request.get_json(force=True)
    json=ccj(json)
    assert json != None
    page=json.get("page")
    limit=json.get("limit")
    if page == None:
        page=0
    else:
        json.__delitem__("page")

    if limit == None:
        limit = 10
    else:
        json.__delitem__("limit")
    ledgers=db.session.query(Ledger).filter_by(**json).limit(limit).offset(page*limit).all()
    if ledgers == []:
        return status(Ledger(),status=status_codes.INVALID_ID,msg="no ledgers could be found!")
    ledgerSchema=LedgerSchema()
    ledgers=[ledgerSchema.dump(i) for i in ledgers]
    return status(Ledger(),status=status_codes.OBJECTS,objects=Json.dumps(ledgers))


@app.route("/ledger/delete/<ledger_id>",methods=["delete"])
@auth.login_required
def delete_ledger(ledger_id): 
    return delete(ledger_id,Ledger)

@app.route("/ledger/update/<ledger_id>/remove/user/<user_id>",methods=["get"])
@auth.login_required
def remove_user_to_ledger(ledger_id,user_id):
    assert ledger_id != None
    assert user_id != None
    user=db.session.query(User).filter_by(id=user_id).first()
    assert user != None
    ledger=db.session.query(Ledger).filter_by(id=ledger_id).first()
    #removal=False
    print(ledger.user)
    try:
        ledger.user.remove(user)
    except:
        return status(ledger,status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(ledger,status=status_codes.UPDATED)

@app.route("/ledger/update/<ledger_id>/add/user/<user_id>",methods=["get"])
@auth.login_required
def add_user_to_ledger(ledger_id,user_id):
    assert ledger_id != None
    assert user_id != None
    user=db.session.query(User).filter_by(id=user_id).first()
    assert user != None
    ledger=db.session.query(Ledger).filter_by(id=ledger_id).first()
    print(ledger.user)
    if user not in ledger.user:
        ledger.user.append(user)
    else:
        return status(ledger,status=status_codes.NOT_UPDATED) 
    flag_modified(ledger,"user")
    db.session.merge(ledger)
    db.session.flush()
    db.session.commit()
    return status(ledger,status=status_codes.UPDATED)

@app.route("/ledger/update/<ledger_id>/remove/productCount/<product_count_id>",methods=["get"])
@auth.login_required
def remove_product_to_ledger(ledger_id,product_count_id):
    assert ledger_id != None
    assert product_count_id != None
    product=db.session.query(ProductCount).filter_by(id=product_count_id).first()
    assert product != None
    ledger=db.session.query(Ledger).filter_by(id=ledger_id).first()
    #removal=False
    print(ledger.productCount)
    try:
        ledger.productCount.remove(product)
    except:
        return status(ledger,status=status_codes.NOT_UPDATED)
    
    db.session.commit()
    return status(ledger,status=status_codes.UPDATED)

@app.route("/ledger/update/<ledger_id>/add/productCount/<product_count_id>",methods=["get"])
@auth.login_required
def add_product_to_ledger(ledger_id,product_count_id):
    assert ledger_id != None
    assert product_count_id != None
    product=db.session.query(ProductCount).filter_by(id=product_count_id).first()
    assert product != None
    ledger=db.session.query(Ledger).filter_by(id=ledger_id).first()
    print(ledger.productCount)
    if product not in ledger.productCount:
        ledger.productCount.append(product)
    else:
        return status(ledger,status=status_codes.NOT_UPDATED)

    flag_modified(ledger,"productCount")
    db.session.merge(ledger)
    db.session.flush()
    db.session.commit()
    return status(ledger,status=status_codes.UPDATED)


