# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class Scope(object):
    key = None
    attributes = ()

    def produce(self, user_object):
        res = {}
        for label, data_key in self.attributes:
            if data_key:
                data_value = getattr(user_object, data_key, '')
                if hasattr(data_value, '__json__'):
                    data_value = data_value.__json__(None)
                res[label] = data_value
            else:
                # Not implemented
                res[label] = ''
        return res


class OpenIdScope(Scope):
    key = 'openid'
    attributes = (
        ('user_id', 'id'),
    )


class ProfileScope(Scope):
    key = 'profile'
    attributes = (
        ('name', 'label'),
        ('firstname', 'firstname'),
        ('lastname', 'lastname'),
        ('email', 'email'),
        ('login', 'login'),
        # ('groups', 'groups'),
    )
