# -*- coding: utf-8 -*-
from cinder import context
from oslo_config import cfg
import pyotp
import webob


# For compatibility with Cinder
use_forwarded_for_opt = cfg.BoolOpt(
    'use_forwarded_for',
    default=False,
    help='Treat X-Forwarded-For as the canonical remote address. '
         'Only enable this if you have a sanitizing proxy.')

admin_pwd = cfg.StrOpt(
    'admin_password',
    help='Admin password for user-project admin-admin.')

CONF = cfg.CONF
CONF.register_opts((use_forwarded_for_opt, admin_pwd))


class BaseAuthFilter(object):
    AUTH_TOKEN_HEADER = 'X-Auth-Token'

    def __init__(self, app, passwords, **kwargs):
        pwds = {(user, project): pwd for user, project, pwd in
                (item.split(':', 2) for item in passwords.split())}
        self.admins = []
        admin_password = kwargs.get('admin_password', CONF.admin_password)
        if admin_password:
            admin = ('admin', 'admin')
            pwds[admin] = admin_password
            self.admins.append(admin)

        self.passwords = pwds
        self.app = app

    def _check_password(self, user, project, password):
        raise NotImplemented()

    def _authenticate(self, req):
        token = req.headers.get(self.AUTH_TOKEN_HEADER)
        if not token or token.count(':') < 2:
            msg = ('Header %s must contain User:Project:Password.' %
                   self.AUTH_TOKEN_HEADER)
            raise webob.exc.HTTPForbidden(explanation=msg)
        user, project, pwd = token.split(':', 2)
        try:
            authenticated = self._check_password(user, project, pwd)
        except Exception:
            authenticated = False
        finally:
            if not authenticated:
                msg = ('Wrong User:Project:Password in header %s' %
                       self.AUTH_TOKEN_HEADER)
                raise webob.exc.HTTPForbidden(explanation=msg)
        is_admin = (user, project) in self.admins
        return user, project, pwd, is_admin

    @webob.dec.wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        user, project, pwd, is_admin = self._authenticate(req)
        remote_address = getattr(req, 'remote_address', '127.0.0.1')
        if CONF.use_forwarded_for:
            remote_address = req.headers.get('X-Forwarded-For', remote_address)
        ctx = context.RequestContext(user,
                                     project,
                                     is_admin=is_admin,
                                     remote_address=remote_address)
        req.environ['cinder.context'] = ctx
        return self.app

    @classmethod
    def factory(cls, global_conf, passwords):
        def filter(app):
            return cls(app, passwords)
        return filter


class PlainPasswordAuthFilter(BaseAuthFilter):
    def _check_password(self, user, project, password):
        return self.passwords[(user, project)] == password


class OTPAuthFilter(BaseAuthFilter):
    def __init__(self, app, passwords, **kwargs):
        super(OTPAuthFilter, self).__init__(app, passwords, **kwargs)
        # To reduce runtime work we generate all the OTPs
        for key, base32secret in self.passwords.items():
            self.passwords[key] = pyotp.TOTP(base32secret)

    def _check_password(self, user, project, password):
        totp = self.passwords[(user, project)]
        return totp.verify(password)
