from werkzeug.security import safe_str_cmp;
from src_1.models.user import UserModel;


# given a username and password, select user
def authenticate(username,password):
    user = UserModel.find_by_username(username)
    #print ("User given password ", password)
    #print ("Password in db ", user.password )

    if user !=None and (safe_str_cmp(user.password,password)):
        return user
    print("Password DOES NOT match")
    return False

def identity(payload):
    user_id = payload['identity']
    print ("Checking identity", user_id)
    return UserModel.find_by_id(user_id)
