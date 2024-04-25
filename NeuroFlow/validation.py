import re
import json
import jwt
import datetime
from flask import request
import string
import random

from NeuroFlow.database import *

def RequiredToken(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                token = token.split(' ')[1]
                data = jwt.decode(token, 'secret', algorithms=['HS256'])
                print(data)
                if datetime.datetime.fromtimestamp(data['exp']) < datetime.datetime.utcnow():
                    return json.dumps({"status":401 ,"message":"Token Expired"})

                if not checkIDSQL(data['uid']):
                    return json.dumps({"status":498,"message":"Invalid Token"})
                return f(*args, **kwargs)
            except Exception as e:
                print("ErroADAWDWADr")
                print(e)
                return json.dumps({"status":498,"message":"Invalid Token"})
        else:
            return json.dumps({"status":101,"message":"Token Required"})
    wrapper.__name__ = f.__name__
    return wrapper

def codeGenerate():
    letters = string.ascii_lowercase
    numbers = string.digits
    code = ''.join(random.choice(letters) for i in range(2)) + ''.join(random.choice(numbers) for i in range(3))
    return code.upper()