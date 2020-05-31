from .models.user import auth,db,User

def roles_required(roles:list,**arguments):
    def decorator(function):
        def Wrapper(*args,**kargs): 
            #roles=arguments.get("roles")
            uname=auth.username()
            user=db.session.query(User).filter_by(uname=uname).first()
            print(user.roles)
            authorized=False
            for i in roles:
                for ii in user.roles:
                    if ii.name == i:
                        authorized=True
                        break
            else:
                if roles == []:
                    authorized=True

            if authorized == False:
                return "user not authorized by role!",401
            r=function(*args,**kargs)
            return r
        Wrapper.__name__ = function.__name__
        return Wrapper
    return decorator


