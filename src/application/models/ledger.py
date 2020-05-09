from .. import db,auth,ma
from .productCount import ProductCount,ProductCountSchema
from .user import User,UserSchema
from .as_dict import AsDict

ledger_productCount=db.Table("ledger_products",
        db.Column("ledger_id",db.Integer,db.ForeignKey("ledger.id")),
        db.Column("productCount_id",db.Integer,db.ForeignKey("productCount.id"))
    )
ledger_user=db.Table("ledger_user",
        db.Column("ledger_id",db.Integer,db.ForeignKey("ledger.id")),
        db.Column("user_id",db.Integer,db.ForeignKey("users.id"))
    )

class Ledger(db.Model,AsDict):
    __tablename__="ledger"
    id=db.Column(db.Integer,primary_key=True)
    timestamp=db.Column(db.DateTime)
    productCount=db.relationship('ProductCount',secondary=ledger_productCount,backref=db.backref("ledger"))
    user=db.relationship('User',secondary=ledger_user,backref=db.backref("ledger"))
    

    def __repr__(self):
        return """
            Ledger(
                id={},
                timestamp={}
                productCount={}
                user={}
            )
        """.format(self.id,self.timestamp,self.productCount,self.user)

class LedgerSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Ledger
    id=ma.auto_field()
    timestamp=ma.auto_field()
    productCount=ma.List(ma.Nested(ProductCountSchema))
    user=ma.List(ma.Nested(UserSchema))

