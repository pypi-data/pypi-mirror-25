import click

from dashops.common.utils import execute_command, export_common_envs
from dashops.main import root
from dashops.parameters import ClusterNameParamType
from dashops.services import KopsService


@root.command('edit')
@click.argument('cluster-name', type=ClusterNameParamType(), nargs=1, expose_value=True)
@click.option('--s3-bucket', type=click.STRING,
              help='Specify the bucket to store cluster state.\nDefaults to cluster-name.')
@click.option('--yes', is_flag=True, help='If to apply immediately.')
def edit(cluster_name, s3_bucket, yes):
    """
    Edit a cluster config.
    """
    if not s3_bucket:
        s3_bucket = cluster_name
    export_common_envs(cluster_name, s3_bucket)
    execute_command(KopsService.get_edit_command(cluster_name))
    if yes:
        execute_command(KopsService.get_update_command(cluster_name, True))
