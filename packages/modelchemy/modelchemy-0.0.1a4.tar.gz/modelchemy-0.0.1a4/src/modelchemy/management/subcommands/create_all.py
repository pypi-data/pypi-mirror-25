# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from modelchemy import dbs
from modelchemy.management.subcommands.base import BaseSubCommand


class CreateAllSubCommand(BaseSubCommand):
    help = 'Creates the tables in Metadata object'

    @property
    def subcommand(self):
        return 'create-all'

    def handle(self, *args, **options):
        self.stdout.write('Metadata Dump to Db Started')
        dbs.get(self._database).metadata.create_all()
        self.stdout.write('Metadata Dump to Db Finished')


