# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2017 KeyIdentity GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@keyidentity.com
#    Contact: www.linotp.org
#    Support: www.keyidentity.com
#

""" This file containes PasswordTokenClass """

import logging
from linotp.lib.crypto import zerome
from linotp.lib.util import getParam


optional = True
required = False

from linotp.lib.tokenclass import TokenClass
from linotp.lib.tokens.hmactoken import HmacTokenClass

log = logging.getLogger(__name__)

###############################################


class PasswordTokenClass(HmacTokenClass):
    '''
    This Token does use a fixed Password as the OTP value.
    In addition, the OTP PIN can be used with this token.
    This Token can be used for a scenario like losttoken
    '''

    class __secretPassword__(object):

        def __init__(self, secObj):
            self.secretObject = secObj

        def getPassword(self):
            return self.secretObject.getKey()

        def checkOtp(self, anOtpVal):
            res = -1

            key = self.secretObject.getKey()

            if key == anOtpVal:
                res = 0

            zerome(key)
            del key

            return res

    def __init__(self, aToken):
        TokenClass.__init__(self, aToken)
        self.hKeyRequired = True
        self.setType(u"pw")

    @classmethod
    def getClassType(cls):
        return "pw"

    @classmethod
    def getClassInfo(cls, key=None, ret='all'):
        '''
        getClassInfo - returns a subtree of the token definition

        :param key: subsection identifier
        :type key: string

        :param ret: default return value, if nothing is found
        :type ret: user defined

        :return: subsection if key exists or user defined
        :rtype: s.o.

        '''

        res = {
            'type': 'pw',
            'title': 'Password Token',
            'description': ('A token with a fixed password. Can be combined with the OTP PIN. Is used for the lost token scenario.'),
            'init': {},
            'config': {},
            'selfservice':  {},
            'policy': {},
        }
        # I don't think we need to define the lost token policies here...

        if key is not None and res.has_key(key):
            ret = res.get(key)
        else:
            if ret == 'all':
                ret = res
        return ret

    def update(self, param):

        TokenClass.update(self, param)
        # The otplen is determined by the otpkey. So we
        # call the setOtpLen after the parents update, to overwrite
        # specified OTP lengths with the length of the password
        self.setOtpLen(0)

    def setOtpLen(self, otplen):
        '''
        sets the OTP length to the length of the password
        '''
        secObj = self._get_secret_object()
        sp = PasswordTokenClass.__secretPassword__(secObj)
        pw_len = len(sp.getPassword())
        TokenClass.setOtpLen(self, pw_len)
        return

    def checkOtp(self, anOtpVal, counter, window, options=None):
        '''
        This checks the static password
        '''

        secObj = self._get_secret_object()
        sp = PasswordTokenClass.__secretPassword__(secObj)
        res = sp.checkOtp(anOtpVal)

        return res
