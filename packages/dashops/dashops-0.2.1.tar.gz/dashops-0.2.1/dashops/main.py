import os
import sys

import click

from dashops.constants import DASHOPS_VERSION

cmd_folder = os.path.join(os.path.dirname(__file__), 'cmd')


class ComplexCLI(click.Group):
    def list_commands(self, ctx):
        rv = []
        if not os.path.isdir(cmd_folder):
            return rv
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
            if os.path.isdir(os.path.join(cmd_folder, filename)):
                rv.append(filename)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            func_name = "{}".format(name)
            if func_name.startswith('_'):
                return
            import_path = "dashops.cmd.{}".format(name)
            mod = __import__(import_path, None, None, [func_name])
        except ImportError:
            return
        try:
            mod = getattr(mod, func_name)
        except AttributeError:
            return
        return mod


def modify_usage_error():
    """
    Function to modify the default click error handling.
    Used here to tell the user about how to find additional help.
    With thanks to this Stack Overflow answer: http://stackoverflow.com/a/43922088/713980
    :return: None
    """

    def show(self, file=None):
        if file is None:
            file = click._compat.get_text_stderr()
        color = None
        if self.ctx is not None:
            color = self.ctx.color
            click.secho(self.ctx.get_help() + '\n', file=file, color=color)
        click.secho('Error: %s' % self.format_message(), fg='red', file=file, color=color)

    click.exceptions.UsageError.show = show


modify_usage_error()


@click.command(cls=ComplexCLI)
@click.version_option(version=DASHOPS_VERSION, prog_name='dashops')
def root():
    """
    CLI tool to manage a kubernetes cluster using kops on aws.
    """
    pass
