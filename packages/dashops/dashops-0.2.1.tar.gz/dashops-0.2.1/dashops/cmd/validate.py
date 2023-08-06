import click

from dashops.common.utils import execute_command, export_common_envs
from dashops.main import root
from dashops.parameters import ClusterNameParamType
from dashops.services import KopsService


@root.command('validate')
@click.argument('cluster-name', type=ClusterNameParamType(), nargs=1, expose_value=True)
@click.option('--s3-bucket', type=click.STRING,
              help='Specify the bucket to store cluster state.\nDefaults to cluster-name.')
def validate(cluster_name, s3_bucket):
    """
    Delete a cluster.
    """
    if not s3_bucket:
        s3_bucket = cluster_name
    export_common_envs(cluster_name, s3_bucket)
    execute_command(KopsService.get_validate_command(cluster_name))
