from ..models.user import User
from .. import db,auth,app

from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

user_manager=UserManager(app,db,User)


def verify_password(username,password):
    yuser=db.session.query(User).filter(User.uname.in_([username])).first()
    #global authed
    #authed=yuser
    print(yuser)
    if not yuser or not yuser.verify_password(password):
        print("#")
        return dict(user=None,authorized=False)
    if not yuser.active:
        print("$")
        return dict(user=None,authorized=False)
    return dict(user=yuser,authorized=True)

