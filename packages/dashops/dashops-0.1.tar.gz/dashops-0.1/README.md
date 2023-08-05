# dashbase-operator

This tool is currently a wrapper of [kops](https://github.com/kubernetes/kops), which allows user to create multiple kubernetes clusters in one vpc even in one subnet.

It's aim is to make user able to create a cluster like [stackpoint](https://stackpoint.io/). User only needs to do some simple selections and then can get a running cluster.

## Install

`pip install dashops`

## Preparation

First, you need to install [aws-cli](https://github.com/aws/aws-cli)

```
pip install awscli

# on mac
brew install mawscli
```

Second, you need to install [kops](https://github.com/kubernetes/kops), and **configure your aws credientials, set up your aim and export key and secret to env according to the [kops document](https://github.com/kubernetes/kops/blob/master/docs/aws.md)**:

```
aws configure
export AWS_ACCESS_KEY_ID=<access key>
export AWS_SECRET_ACCESS_KEY=<secret key>
```

Thirdly, you need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in order to control your cluster.

## Usage

### create

To create a cluster:

```Shell
dashops create testk8s.example.com
```

**cluster name should obey the rules in kops document(a domain name)!**

More complicated usage:

```
dashops create --s3-bucket testk8s-state-store --num-nodes 5 --zone ap-northeast-1a --region ap-northeast-1 --vpc-id vpc-12345678 --network-cidr 172.31.0.0/16 --subnet-cidr 172.31.0.0/20 --subnet-id subnet-1234abcd --edit testk8s.example.com
```



For more detailed usage:

```
Usage: dashops create [OPTIONS] CLUSTER_NAME

  Create a cluster.

Options:
  --s3-bucket TEXT           Specify the bucket to store cluster state.
                             Defaults to cluster-name.
  --machine-type TEXT        Specify the machine type to use in the cluster.  [default: r4.xlarge]
  --num-nodes INTEGER RANGE  Specify number of nodes to start in the cluster.  [default: 3]
  --zone TEXT                Specify the zone to use.  [default: us-west-1b]
  --region TEXT              Specify the region to use.  [default: us-west-1]
  --vpc-id TEXT              Specify the vpc to use.
  --network-cidr TEXT        Specify the network cidr of vpc.
                             Should match the cidr of specified vpc.
  --subnet-id TEXT           Specify the subnet-id to use.
  --subnet-cidr TEXT         Specify the subnet cidr to create.
                             This will be ignored if "subnet-id" is specified.
  --edit                     If to edit the information before apply on aws.
  --help                     Show this message and exit.
```

### edit

To edit a cluster info:

```
dashops edit testk8s.example.com
```

For more detailed usage:

```
Usage: dashops edit [OPTIONS] CLUSTER_NAME

  Edit a cluster config.

Options:
  --s3-bucket TEXT  Specify the bucket to store cluster state.
                    Defaults to cluster-name.
  --yes             If to apply immediately.
  --help            Show this message and exit.
```

### delete

To delete a cluster:

```
dashops delete testk8s.example.com
```

For more detailed usage:

```
Usage: dashops delete [OPTIONS] CLUSTER_NAME

  Delete a cluster.

Options:
  --s3-bucket TEXT  Specify the bucket to store cluster state.
                    Defaults to cluster-name.
  --yes             If to apply immediately.
  --help            Show this message and exit.
```

### export

To set your kubectl context:

```
dashops export testk8s.example.com
```

For more detailed usage:

```
Usage: dashops export [OPTIONS] CLUSTER_NAME

  Export a cluster's kubeconfig.

Options:
  --s3-bucket TEXT  Specify the bucket to store cluster state.
                    Defaults to cluster-name.
  --path PATH       Specify the path to export to.
                    If the path is a dir, then will save the config to "kubeconfig" under "path", elsethe path is treated as a file path.
  --help            Show this message and exit.
```

