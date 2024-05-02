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
* `helm repo add spark-operator https://kubeflow.github.io/spark-operator`
* `helm install my-release spark-operator/spark-operator --namespace spark-operator --create-namespace`
* Verify spark operator is installed properly by checking the operator pod with the command `kubectl get pods -n ${namespace} | grep spark-operator` this should list the spark-operator pod and status should be `Running` state.

## Installing the chart
## Initialize minio kubernetes operator
* `kubectl minio init --namespace ${your-namespace}` 
* [Validate the operator installation](https://min.io/docs/minio/kubernetes/upstream/operations/installation.html#validate-the-operator-installation) 
## Install play-ground-chart
* Change directory to root of the git repository.
* `helm install --namespace ${your-namespace} --create-namespace play-ground ./play-ground-chart`
* Wait for all the pods to be in Running state. This will take some time.
* Make sure following pods are in running state.
    * Dremio
        * dremio-master-0
        * dremio-executor-0
    * Minio
        * myminio-pool-0-0
        * myminio-pool-0-1
        * myminio-pool-0-2
        * myminio-pool-0-3
    * Hive Meta Store
        * ${release-name}-hive-metastore-0

## Port-forward Dremio & Minio services
* To access Minio & Dremio port-forward following services.
* `kubectl --namespace ${namespace} port-forward svc/myminio-console 9090:9090`
* `kubectl --namespace ${namespace} port-forward svc/dremio-client 9047:9047`

## Access & Configure Dremio
* Once port-forward is done. Dremio UI will be able to access in url `http://localhost:9047`
* This will prompt to create admin user. Set up user.
* Adding Hive Meta Store
    * To add Hive meta store as source. More details refer (here)[https://docs.dremio.com/current/sonar/data-sources/metastores/hive/]
    * Click on `Add Data Soruce`
    * Select Hive3
    * Provide a name
    * Hive Metastore Host put `${release-name-hive-metastore.${namespace}.svc.cluster.local`
    * Click save



# Things to do
* Create job for hive metastore creation
