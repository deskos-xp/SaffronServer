'''
Created on Feb 14, 2020

@author: carl
'''

 
@auth.verify_password
def verify_password(username,password):
    yuser=db.session.query(User).filter(User.uname.in_([username])).first()
    print(yuser.uname)
    if not yuser or not yuser.verify_password(password):
        return False
    return True


@app.route("/new_user",methods=["POST"])
@auth.login_required
def new_user():
    if request.get_data() != None:
            #how to serialize json to User class
            pass
    return "new user created!"
app.run()
