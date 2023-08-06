class KopsService:
    @classmethod
    def get_create_command(cls, cloud, zones, name, num_nodes, machine_type, vpc=None, yes=False):
        cmd = 'kops create cluster --cloud={} --zones={} --name={} --node-count={} --node-size={}'.format(
            cloud, zones, name, num_nodes, machine_type)
        if vpc:
            cmd += ' --vpc={}'.format(vpc)
        if yes:
            cmd += ' --yes'
        return cmd

    @classmethod
    def get_edit_command(cls, name):
        return 'kops edit cluster {}'.format(name)

    @classmethod
    def get_update_command(cls, name, yes=False):
        cmd = 'kops update cluster {}'.format(name)
        if yes:
            cmd += ' --yes'
        return cmd

    @classmethod
    def get_delete_command(cls, name, yes=False):
        cmd = 'kops delete cluster --name {}'.format(name)
        if yes:
            cmd += ' --yes'
        return cmd

    @classmethod
    def get_export_command(cls, name):
        return 'kops export kubecfg --name {}'.format(name)

    @classmethod
    def get_validate_command(cls, name):
        return 'kops validate cluster {}'.format(name)
