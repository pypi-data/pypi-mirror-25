# -*- coding:utf-8 -*-
import click


class CliRuntimeError(click.ClickException):
    """An exception that Click can handle and show to the user."""

    #: The exit code for this exception
    exit_code = 1

    def format_message(self):
        return self.message

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        click.secho('Error: %s' % self.format_message(), fg='red', file=file)


class CliRuntimeWarning(click.ClickException):
    """An exception that Click can handle and show to the user."""

    #: The exit code for this exception
    exit_code = 0

    def format_message(self):
        return self.message

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        click.secho('Warning: %s' % self.format_message(), fg='yellow', file=file)
