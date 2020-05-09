from .. import db,auth,ma
from .priceUnit import PriceUnit,PriceUnitSchema
from .as_dict import AsDict

price_priceUnits=db.Table("price_priceUnits",db.Column("price_id",db.Integer,db.ForeignKey("price.id")),
                    db.Column("priceUnits_id",db.Integer,db.ForeignKey("priceUnits.id"))
                    )

class Price(db.Model,AsDict):
    __tablename__="price"
    id=db.Column(db.Integer,primary_key=True)
    price_unit=db.relationship('PriceUnit',secondary=price_priceUnits,backref=db.backref("Price"))
    value=db.Column(db.Float)

    def __repr__(self):
        return '''
        Price(
            id={},
            price_units={},
            value={}
            )
            '''.format(self.id,self.price_unit,self.value)

class PriceSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Price

    id=ma.auto_field()
    price_unit=ma.List(ma.Nested(PriceUnitSchema))
    value=ma.auto_field()
