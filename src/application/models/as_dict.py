
class AsDict:
    def as_dict(self):
        x={c.name:getattr(self,c.name) for c in self.__table__.columns}
        z={name:getattr(self,name) for name,r in self.__mapper__.relationships.items()}
        return {'relationships':z,'columns':x}

