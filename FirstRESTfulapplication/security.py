from werkzeug.security import safe_str_cmp
from user import User


# table for users
users = [                       
 #   {'id' : 1,'username':'rob','password':'bor' }, as we are importing from User, we can write in thisway

     User(1, 'rob', 'bor')
]

username_mapping = {
  #  'rob':{'id' : 1,'username':'rob','password':'bor'} instead of this we can write in this way

    u.username:u for u in users
}

userid_mapping = { 
  #  1: {'id' : 1,'username':'rob','password':'bor'}    instead of this we can write in this way

    u.id:u for u in users
}

def authenticate(username,password):   # finding the correct username and password
    user = username_mapping.get(username,None) # if there is no username, then it will return None
    if user and safe_str_cmp(user.password,password): # safe_str_cmp it will compare strings
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id,None)
