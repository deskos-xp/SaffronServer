from flask import jsonify
from ..models.product import Product,ProductSchema
from ..models.ledger import Ledger,LedgerSchema
from .. import db,auth,ma
from flask import current_app as app
from sqlalchemy.inspection import inspect
from .. import models
from .. import ccj,status,status_codes
class export:
    export_fmt='json'
    def __init__(self,**kwargs):
        print(kwargs)
        self.__dict__.update(kwargs)

    def WHAT_to_class(self,WHAT):
        if WHAT == 'ledger':
            return Ledger,LedgerSchema()
        if WHAT == 'product':
            return Product,ProductSchema()

    def export(self,ID,WHAT,page,limit):
        if self.export_fmt in ["json","pdf"]:
            return self.export_json(ID,WHAT,page,limit)

    def getSchemas(self,result):
            relationships=inspect(result.__class__).relationships.items()
            for name,r in relationships:
                attr=getattr(result,name)
                #for i in attr:
                #    print(i.__class__.__name__)
            cl=[]
            for i in dir(models):
                cl.append(getattr(models,i))

            schemas=[]
            for cla in cl:
                for x in dir(cla):
                    if 'Schema' in x:
                        schemas.append(getattr(cla,x))
            schemas=set(schemas)
            return schemas

    def searchDict(self,diction,term,replace):
        for k in diction.keys():
            if type(diction[k]) == type(dict()):
                self.searchDict(diction[k],term,replace)
            else:
                if k == term:
                    diction[k]=replace
        return diction

    def export_json(self,ID,WHAT,page,limit):
            WHAT_class=self.WHAT_to_class(WHAT)
            assert WHAT_class != None
            result=db.session.query(WHAT_class[0]).filter_by(id=ID).limit(limit).offset(limit*page).all()
            
            schemas=self.getSchemas(result[0])
            sd={}
            for i in schemas:
                sd[i.Meta.model.__name__]=i
            #print(sd)
            
            exp=[]
            for result_sub in result:
                exp.append(WHAT_class[1].dump(result_sub))
            return status(WHAT_class(),status=status_codes.OBJECT,object=jsonify(exp))
