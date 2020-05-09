from .. import db,auth,ma
from .weightUnit import WeightUnit,WeightUnitSchema
from .as_dict import AsDict

weight_weightUnits=db.Table("weight_weightUnits",db.Column("weight_id",db.Integer,db.ForeignKey("weight.id")),
                    db.Column("weightUnits_id",db.Integer,db.ForeignKey("weightUnits.id"))
                    )

class Weight(db.Model,AsDict):
    __tablename__="weight"
    id=db.Column(db.Integer,primary_key=True)
    weight_unit=db.relationship('WeightUnit',secondary=weight_weightUnits,backref=db.backref("weight"))
    value=db.Column(db.Float)

    def __repr__(self):
        return '''
        Weight(
            id={},
            weight_units={},
            value={}
            )
            '''.format(self.id,self.weight_unit,self.value)

class WeightSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Weight

    id=ma.auto_field()
    weight_unit=ma.List(ma.Nested(WeightUnitSchema))
    value=ma.auto_field()
