# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import sys

import os
from django.core.management import BaseCommand
from django.core.management import CommandError
from django.core.management import CommandParser

from modelchemy import dbs
from modelchemy.management.subcommands.create_all import CreateAllSubCommand
from modelchemy.management.subcommands.drop_all import DropAllSubCommand

MODELCHEMY_COMMANDS = ('create-all', 'drop-all')


class Command(BaseCommand):
    def run_from_argv(self, argv):

        self._called_from_command_line = True

        parser = self.create_parser(argv[0], argv[1])

        options, argv_unknowns = parser.parse_known_args(argv[2:])

        if len(argv_unknowns) == 0:

            if options.traceback:
                raise CommandError('Missing database alias or key.')

            self.stderr.write('CommandError: Missing database alias or key.')
            sys.exit(1)

        new_argv = [argv[0], argv[1]]
        new_argv.extend(argv_unknowns)

        db_id_parser = CommandParser(
            self, prog="%s %s" % (
                os.path.basename(new_argv[0]), new_argv[1]),
            description=self.help or None,
        )
        db_id_parser.add_argument('database', nargs=1)

        parsed_db_id, unparsed = db_id_parser.parse_known_args(new_argv[2:])

        database_id = parsed_db_id.database[0]

        if database_id not in dbs.keys:

            if database_id in MODELCHEMY_COMMANDS:
                if options.traceback:
                    raise CommandError(
                        'Command invocation without database id.')

                self.stderr.write(
                    'CommandError: Command invocation without database id.')
                sys.exit(1)

            if options.traceback:
                raise CommandError('Database alias or key not found.')

            self.stderr.write('CommandError: Database alias or key not found.')
            sys.exit(1)

        db_id_parser = CommandParser(
            self, prog="%s %s %s" % (
                os.path.basename(new_argv[0]), new_argv[1],
                database_id),
            description=self.help or None,
        )
        db_id_parser.add_argument('cmd', nargs=1)

        parsed_db_id, unparsed = db_id_parser.parse_known_args(unparsed)

        subcmd = parsed_db_id.cmd[0]

        if subcmd not in MODELCHEMY_COMMANDS:
            if options.traceback:
                raise CommandError('Invalid Command.')

            self.stderr.write('CommandError: Invalid Command.')
            sys.exit(1)

        self.handle_subcommnad(argv[0], argv[1], database_id, options, subcmd,
                               unparsed)

    def handle_subcommnad(self, root, cmd, database, options, subcmd, argvs):
        cmd_type = None

        if subcmd == 'create-all':
            cmd_type = CreateAllSubCommand(root, cmd, database,
                                      options, self.stdout, self.stderr,
                                      True)
        elif subcmd == 'drop-all':
            cmd_type = DropAllSubCommand(root, cmd, database, options,
                                          self.stdout, self.stderr, True)

        if cmd_type is not None:
            cmd_type.run_from_argv(argvs)
        else:
            if options.traceback:
                raise CommandError('Invalid Command.')

            self.stderr.write('CommandError: Invalid Command.')
            sys.exit(1)
