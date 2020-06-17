from Mati.model import User
import re

class EmailValidator:

    ''' Check if emails are related on normal email addresses '''

    def checkEmail(self, email):
        checker = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        msg = ""
        if re.search(checker, email):
            msg = "Email is valid!"
        else:
            msg = "Email is not valid"

        return msg

class UniqueUsername:

    ''' Check if username exist on registration process as any user needs to have unique username '''

    def checkUsername(self, username):
        users = User.query.all()
        msg = ""

        for user in users:
            if username == user.username:
                msg = "Username exist"
            else:
                msg = "Username don't exist"
        
            return msg
        
        