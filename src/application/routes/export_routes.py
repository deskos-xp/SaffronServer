from .. import db,auth,ma
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
from flask import send_file,send_from_directory,jsonify,request,make_response
from . import verify
from .. import ccj,status,status_codes

from ..models.user import User
from ..models.product import Product,ProductSchema
from ..models.ledger import Ledger,LedgerSchema
from .exporter import export
from ..tools.sendmsg.msg import sender
from ..tools.reporting.report import gen
import json
from flask  import send_from_directory
import phonenumbers,emails

FMTS=['json','pdf']
WHATS=['product','ledger']

def exportable(FMT):
    return FMT in FMTS

def validWhats(WHAT):
    return WHAT in WHATS

@auth.verify_password
def v(username,password):
    return verify.verify_password(username,password)['authorized']

@app.route("/export/<FMT>/ledger/<UID>/<WHO>/<TO>",methods=["get"])
@auth.login_required
def export_to_text(FMT,UID,WHO,TO):
    assert FMT != None 
    assert UID != None
    assert WHO != None
    assert TO != None
    if not exportable(FMT):
        return status(None,status=status_codes.INVALID_EXPORT_FMT,msg="invalid export fmt")
    e=export(export_fmt=FMT)
    data=e.export(UID,'ledger',0,20)
    z=[]
    for i in data.response:
        d=json.loads(i.decode('utf-8'))
        for ii in d:
            for iii in ii['productCount']:
                for iiii in iii['products']:
                    z.append(
                        (
                            iiii['name'],
                            str(iiii['weight'][0]['value']),
                            iiii['weight'][0]['weight_unit'][0]['name'],
                            iiii['upc'],
                            str(iii['cases']),
                            str(iii['units'])
                        )
                    )
    msg=json.dumps(z)
    zz=[]
    for i in z:
        zz.append(' - '.join(i))
    
    if WHO == "pdf" and FMT == "pdf":
        fname="ledger.pdf"
        doc=gen(zz,"Product Inventory ID:{}".format(UID),os.path.join(app.config['UPLOAD_FOLDER'],fname))
        #send document to curl
        return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']),fname)
    
    if TO in ["phone","email"]:
        method=phone_or_email(WHO,TO)
        if FMT == "pdf":
            fname="ledger.pdf"
            doc=gen(zz,"Product Inventory ID:{}".format(UID),os.path.join(app.config['UPLOAD_FOLDER'],fname))
            #send to where base off of WHO
            #parse who as phonenumber 
            #parse who as email
            #the first to be valid will be the transmission method
            if TO == "email":
                sender(send_type="email",attachment=doc.fname).send(
                        "inventory report!",
                        method,app.config['MESSAGING_EMAIL'],
                        app.config['MESSAGING_PASSWORD'],'')
            else:
                return status(None,status=status_codes.INVALID_FMT_FOR_TO,msg="invalid FMT for TO")
        elif FMT == "txt":
            msg_final='\n'.join(zz)
            sender().send(msg_final,method[0],app.config['MESSAGING_EMAIL'],app.config['MESSAGING_PASSWORD'],method[1])     
    return status(None,status=status_codes.EXPORTING.format(WHO),msg="exported data being transmitted to {}".format(WHO))

def verify_phone_number(number:str,region:str):
    numbers=[i.raw_string for i in phonenumbers.PhoneNumberMatcher(number,region)]  
    assert numbers != []
    return numbers

def verify_email_address(address):
    assert address != None
    if '@' in emails.utils.parseaddr(address)[1]:
        return address
    raise ValueError

def phone_or_email(WHO,TO):
    if TO == "phone":
        return [verify_phone_number(getAddress(WHO,TO),getAddress(WHO,"region"))[0],getAddress(WHO,"carrier")]
    elif TO == "email":
        return verify_email_address(getAddress(WHO,TO))
    raise ValueError

def getAddress(WHO,TO):
    user=db.session.query(User).filter_by(id=WHO).first()
    assert user != None
    return getattr(user,TO)


@app.route("/export/<FMT>/<WHAT>/<ID>",methods=["get","post"])
@auth.login_required
def exporter(FMT,WHAT,ID):
    page=0
    limit=10
    if request.method.lower == 'post':
        json=request.get_json(Force=True)
        json=ccj(json)
        if json.get('page') != None:
            page=json.get('page')
        if json.get("limit") != None:
            limit=json.get("limit")

    assert FMT != None
    assert WHAT != None
    assert ID != None
    if not exportable(FMT):
        return status(None,status=status_codes.INVALID_EXPORT_FMT,msg="invalid export format")
    if not validWhats(WHAT):
        return status(None,status=status_codes.INVALID_EXPORT_OBJ_TYPE,msg="invalid object type to export")
    e=export(export_fmt=FMT)
    return e.export(ID,WHAT,page,limit)

