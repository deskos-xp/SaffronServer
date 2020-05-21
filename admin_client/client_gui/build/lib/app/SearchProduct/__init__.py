import enum
class SearchModeEnum(enum.Enum):
    GET=enum.auto()
    POST=enum.auto()
    DEFAULT=enum.auto()

def mode(data:dict) -> bool: 
    countTrue=0
    for k in data.keys():
        if data.get(k) == True:
            countTrue+=1
    if countTrue > 0: 
        if countTrue == 1:
            if "ID" in data.keys() and data.get("ID") == True:
                return False
        return True
    else:
        return False
    
