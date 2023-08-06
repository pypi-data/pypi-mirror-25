# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import sys

import os
from django.core.exceptions import ImproperlyConfigured
from django.core.management import CommandParser, CommandError, color_style
from django.core.management.base import SystemCheckError
from django.core.management.color import no_style
from django.db import connections


class BaseSubCommand(object):
    help = ''
    _called_from_command_line = False

    def create_parser(self):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = CommandParser(
            self, prog="%s %s %s %s" % (
                os.path.basename(self._root), self._cmd, self._database,
                self.subcommand),
            description=self.help or None,
        )

        self.add_arguments(parser)

        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """

        self._called_from_command_line = True
        parser = self.create_parser()

        options = parser.parse_args(argv)
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            if self._django_options.traceback or not isinstance(e, CommandError):
                raise

            # SystemCheckError takes care of its own formatting.
            if isinstance(e, SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)
        finally:
            try:
                connections.close_all()
            except ImproperlyConfigured:
                # Ignore if connections aren't setup at this point (e.g. no
                # configured settings).
                pass

    def execute(self, *args, **options):

        output = self.handle(*args, **options)
        if output:
            self.stdout.write(output)

        return output

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            'subclasses of BaseCommand must provide a handle() method')

    @property
    def subcommand(self):
        raise NotImplemented

    def __init__(self, root, cmd, database, options, stdout=None, stderr=None,
                 no_color=False):
        self._root = root
        self._cmd = cmd
        self._database = database
        self._django_options = options

        self.stdout = stdout
        self.stderr = stderr

        if no_color:
            self.style = no_style()
        else:
            self.style = color_style()
            self.stderr.style_func = self.style.ERROR