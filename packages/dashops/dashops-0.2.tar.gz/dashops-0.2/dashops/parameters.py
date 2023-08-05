import re

import click


class ClusterNameParamType(click.ParamType):
    name = 'name'
    REGEX = r'^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$'

    def convert(self, value, param, ctx):
        if not re.match(self.REGEX, value):
            self.fail(
                """"{}" is not a valid cluster name supported by kops.""".format(
                    value), param, ctx)
        return value
