from . import config
import app
import hashlib


class Login:
    def __init__(self):
        pass

    @staticmethod
    def GET(*a):
        message = None
        return config.render.login(message)

    @staticmethod
    def POST(*a):
        i = config.web.input()
        pwdhash = hashlib.md5(i.password + config.secret_key).hexdigest()
        check = config.model.validate_user(i.username, pwdhash)
        if check:
            app.session.loggedin = True
            app.session.username = check['username']
            app.session.privilege = check['privilege']
            res = config.model_logs.insert_logs(check['username'])
            print "Logs " + res
            if check['status'] == 0:
                message = "User account disabled!!!!"
                return config.render.login(message)
            else:
                raise config.web.seeother('/admin')
        else:
            message = "User or Password are not correct!!!!"
            return config.render.login(message)
