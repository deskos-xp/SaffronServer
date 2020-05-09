from .. import db,ma,auth
from .as_dict import AsDict

class Department(db.Model,AsDict):
    __tablename__="departments"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(length=128))
    store_department_number=db.Column(db.Integer)
    comment=db.Column(db.String(255))
    
    def __repr__(self):
        return 'Department(name="{0}",store_department_number={1},comment="{2},id={3}"'.format(self.name,self.store_department_number,self.comment,self.id)

    def defaultdict(self):
        return dict(name=str(),store_department_number=int(),comment=str(),id=int())

class DepartmentSchema(ma.SQLAlchemySchema): 
    class Meta:
        model=Department
    id=ma.auto_field()
    name=ma.auto_field()
    store_department_number=ma.auto_field()
    comment=ma.auto_field()
