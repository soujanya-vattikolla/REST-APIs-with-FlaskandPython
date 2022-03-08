from werkzeug.security import safe_str_cmp
from Storedata_SQLDB.user import User



def authenticate(username,password):   # finding the correct username and password
    user = User.find_by_username(username) # if there is no username, then it will return None
    if user and safe_str_cmp(user.password,password): # safe_str_cmp it will compare strings
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
