# -*- coding: utf-8 -*-
import cinder_auths

__all__ = ('__author__', '__email__', '__version__',
           'otp_factory', 'single_pwd_factory')

__author__ = """Gorka Eguileor"""
__email__ = 'gorka@eguileor.com'
__version__ = '0.1.1'

otp_factory = cinder_auths.OTPAuthFilter.factory
plain_pwd_factory = cinder_auths.PlainPasswordAuthFilter.factory
