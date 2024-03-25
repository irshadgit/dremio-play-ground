# dremio-play-ground
Consist of helm chart to install following components.

# How to install the chart?

## Pre-requisites
* An existing Kubernetes cluster. Version v1.23.3 or later.
    * You can use [minikube](https://minikube.sigs.k8s.io/docs/start/) to create local kubernetes cluster.
### Install minio kuberenetes plugin
* Install kubectl plugin manager [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/) - 
* Install minio kubernetes plugin using krew as described [here](https://min.io/docs/minio/kubernetes/upstream/operations/installation.html#install-the-minio-kubernetes-plugin)
* Verify plugin installation using command `kubectl minio version`
### Install spark operator
* helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
* helm install spark-operator spark-operator/spark-operator --namespace ${name_space} --set webhook.enable=true --set image.repository=openlake/spark-operator --set image.tag=3.3.1 --create-namespace

## Installing the chart
## Initialize minio kubernetes operator
* `kubectl minio init --namespace ${your-namespace}` 
* [Validate the operator installation](https://min.io/docs/minio/kubernetes/upstream/operations/installation.html#validate-the-operator-installation) 
## Install play-ground-chart
* Change directory to root of the git repository.
* `helm install --namespace ${your-namespace} --create-namespace play-ground ./play-ground-chart`
* kubectl --namespace play-ground port-forward svc/myminio-console 9443:9443
* kubectl port-forward svc/myminio-hl 9000 -n minio


# Things to do
* Create job for hive metastore creation
* Completes the S3 bucket creation and sample S3 file loads.
* Job to loads the Iceberg tables from the S3 loaded data sets.
# Issue encoutnered 
* https based access was failing. Disabled ssl for minio using helm chart.
Settings for spark accessing minio
    hadoopConf.set("fs.s3a.access.key", "minio")
    hadoopConf.set("fs.s3a.secret.key", "minio123")
    hadoopConf.set("fs.s3a.endpoint", "http://localhost:9443")
    hadoopConf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoopConf.set("fs.s3a.path.style.access", "true")
* Dremio helm chart issues:

    * Service has to be changed to type: ClusterIP
    * CPU and ram settings has to be reduced. Else pods were staying in pending state without scheduling.
    * Minio connectivity issues below extraProperties have worked - https://community.dremio.com/t/s3-like-storage-for-distributed-storage/9212/3?u=irshad-pai

minio mc command
mc alias set myminio http://myminio-hl.play-ground.svc.cluster.local:9000 minio minio123 --insecure


--- Sanchith Issues

* Remove namespace hard coding from metastore config minio
* Create warehouse & test bucket with proper names
* Create Hive metastore using REST API

---
* Auto create Iceberg tables
* Create Hive metastore using REST API
* Add airflow


