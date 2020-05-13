from .. import db,auth,ma
from .as_dict import AsDict

class WeightUnit(db.Model,AsDict):
    __tablename__="weightUnits"
    name=db.Column(db.String(length=10))
    symbol=db.Column(db.String(length=10))
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String(length=255))
    
    def __repr__(self):
        return """
        WeightUnit(
        name="{}",
        symbol=b'{}',
        id={}
        comment="{}"
        )
        """.format(self.name,self.symbol,self.id,self.comment)

class WeightUnitSchema(ma.SQLAlchemySchema):
    class Meta:
        model=WeightUnit
    name=ma.auto_field()
    symbol=ma.auto_field()
    id=ma.auto_field()
    comment=ma.auto_field()
