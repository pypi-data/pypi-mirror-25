import os
import shutil

import click

from dashops.common.utils import execute_command, export_common_envs
from dashops.main import root
from dashops.parameters import ClusterNameParamType
from dashops.services import KopsService


@root.command('export')
@click.argument('cluster-name', type=ClusterNameParamType(), nargs=1, expose_value=True)
@click.option('--s3-bucket', type=click.STRING,
              help='Specify the bucket to store cluster state.\nDefaults to cluster-name.')
@click.option('--path', type=click.Path(exists=False, file_okay=True, dir_okay=True, writable=True, resolve_path=True),
              help='Specify the path to export to.\nIf the path is a dir, then will save the config to "kubeconfig" under "path", else the path is treated as a file path.')
def export(cluster_name, s3_bucket, path):
    """
    Export a cluster's kubeconfig.
    """
    if not s3_bucket:
        s3_bucket = cluster_name
    if not path:
        path = os.getcwd()
    export_common_envs(cluster_name, s3_bucket)
    execute_command(KopsService.get_export_command(cluster_name))

    # copy kubeconfig to path
    kube_path = os.path.abspath(os.path.join(os.path.expanduser('~'), '.kube', 'config'))
    dst = path
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isdir(path):
        dst = os.path.join(os.path.dirname(path), 'kubeconfig')
    if kube_path != path:
        shutil.copy(kube_path, dst)
