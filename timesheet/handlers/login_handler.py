from tornado.httputil import HTTPInputError
from sqlalchemy.orm.exc import NoResultFound

from timesheet.handlers.base_handler import BaseHandler
from timesheet.model.user import User
from timesheet.utils.user_session import user_session

__author__ = 'James Stidard'


class LoginHandler(BaseHandler):

    def put(self):
        username = self.get_json_argument('username')
        password = self.get_json_argument('password')
        import logging
        logging.info('username: {}, password: {}'.format(username, password))
        with self.control.session as session:
            try:
                user = session.query(User)\
                              .filter(User.username == username).one()
                user.authenticate(password)
                session.commit()
            except (NoResultFound, ValueError):
                raise HTTPInputError('Incorrect username or password')
            else:
                self.set_secure_cookie('user_id', user.id)
                self.write('Success')

    @user_session
    def delete(self, session, user):
        self.clear_cookie('user_id')
