import boto3


class SubnetService:
    @classmethod
    def list_subnet(cls, vpc_id, region_name=None):
        if region_name is None:
            region_name = 'us-west-1'
        ec2 = boto3.resource('ec2', region_name=region_name)
        vpc = ec2.Vpc(vpc_id)
        return [subnet.id for subnet in vpc.subnets.all()]

    @classmethod
    def get_subnet_cidr(cls, subnet_id, region_name=None):
        if region_name is None:
            region_name = 'us-west-1'
        ec2 = boto3.resource('ec2', region_name=region_name)
        subnet = ec2.Subnet(subnet_id)
        return subnet.cidr_block
