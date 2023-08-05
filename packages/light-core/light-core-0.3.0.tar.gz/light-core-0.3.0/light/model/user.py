import logging

from light.model.datarider import Rider
from light.error.db import NotExist, NotCorrect
from light.crypto import Crypto
from light.configuration import Config


class User(object):
    def __init__(self):
        self.rider = Rider.instance()

    def verify(self, handler):
        condition = {'condition': {'id': handler.params.id}}
        user, error = self.rider.user.get(handler.copy(condition))

        if error:
            logging.warning('Unable to retrieve the user.')
            return None, error

        if user is None:
            logging.warning('User does not exist.')
            return None, NotExist()

        password = handler.params.password
        hmackey = handler.params.hmackey
        if not hmackey:
            hmackey = Config.instance().app.hmackey

        if user['password'] != Crypto.sha256(password, hmackey):
            logging.warning('The user password is not correct.')
            return None, NotCorrect()

        del user['password']
        self.setup_session(handler, user)

        return user, None

    @staticmethod
    def setup_session(handler, user):
        session = handler.session

        session['user'] = user
        session['code'] = handler.code
        session['domain'] = handler.domain

    @staticmethod
    def clear_session(handler):
        del handler.session['user']
        del handler.session['code']
        del handler.session['domain']
