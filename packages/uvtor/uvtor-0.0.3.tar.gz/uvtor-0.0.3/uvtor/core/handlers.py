from uvtor.conf import settings
import tornado.web
import functools


class BaseHandler(tornado.web.RequestHandler):

    def check_xsrf_cookie(self):

        if settings.DEBUG:
            return True
        else:
            super(BaseHandler, self).check_xsrf_cookie()

    def _args(self, *keys):
        return map(
            functools.partial(
                self.get_argument, default=None),
            keys)

    def _secure_cookies(self, *keys):
        return map(
            self.get_secure_cookie,
            keys)
