# -* encoding: utf-8 *-
from __future__ import absolute_import
import warnings

from django.apps import AppConfig
from django.db.backends.postgresql.base import DatabaseWrapper as PostgreSQLDatabaseWrapper
from django.db.backends.signals import connection_created
from typing import Any, Type


warning_given = False


def setrole_connection( **kwargs):
    connection = kwargs['connection']; del kwargs['connection']
    sender = kwargs['sender']; del kwargs['sender']
    global warning_given
    role = None
    if u"set_role" in connection.settings_dict:
        role = connection.settings_dict[u"set_role"]
    elif u"SET_ROLE" in connection.settings_dict:
        role = connection.settings_dict[u"SET_ROLE"]

    if role:
        connection.cursor().execute(u"SET ROLE %s", (role,))
    else:
        if not warning_given:
            warnings.warn(u"postgresql_setrole27 app is installed, but no SET_ROLE value is in settings.DATABASE")
            warning_given = True  # Once is enough


class DjangoPostgreSQLSetRoleApp(AppConfig):
    name = u"postgresql_setrole27"

    def ready(self):
        connection_created.connect(setrole_connection, sender=PostgreSQLDatabaseWrapper)


default_app_config = u'postgresql_setrole27.DjangoPostgreSQLSetRoleApp'
