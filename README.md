# dremio-play-ground
Consist of helm chart to install following components.

# How to install the chart?

## Pre-requisites
* An existing Kubernetes cluster. Version v1.23.3 or later.
    * You can use [minikube](https://minikube.sigs.k8s.io/docs/start/) to create local kubernetes cluster.
### Install minio-operator
* Add helm repo - `helm repo add minio-operator https://operator.min.io`
* `helm install --namespace ${namespace} --create-namespace operator minio-operator/operator`
* Verify minio-operator installation by checking `kubectl get pods -n ${namespace}`
* There should be following pods up and running if installation is succesfull.

| Pod Name                         | Status   | Age  |
|----------------------------------|----------|------|
| pod/console-68d955874d-vxlzm     | Running  | 25h  |
| pod/minio-operator-699f797b8b-th5bk | Running | 25h  |
| pod/minio-operator-699f797b8b-nkrn9 | Running | 25h  |


### Install spark operator
* helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
* helm install spark-operator spark-operator/spark-operator --namespace ${name_space} --set webhook.enable=true --set image.repository=openlake/spark-operator --set image.tag=3.3.1 --create-namespace
* Verify spark operator is installed properly by checking the operator pod with the command `kubectl get pods -n ${namespace} | grep spark-operator` this should list the spark-operator pod and status should be `Running` state.

## Installing the chart
## Initialize minio kubernetes operator
* `kubectl minio init --namespace ${your-namespace}` 
* [Validate the operator installation](https://min.io/docs/minio/kubernetes/upstream/operations/installation.html#validate-the-operator-installation) 

## Install chart dependencies
* Run command from root directory to update dependencies `helm dependency update -n ${name-space} ./play-ground-chart/`
* Build dependencies `helm dependency build -n ${name-space} ./play-ground-chart/`
* This will build and install all dependencies charts from helm repository. Eg: PostgreSQL.

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
    * Apache Airflow
        * ${release-name}-scheduler
        * ${release-name}-worker
        * ${release-name}-trigerer
        * ${release-name}-scheduler

## Port-forward Dremio & Minio services
* To access Minio, Dremio & Airflow port-forward following services.
* `kubectl --namespace ${namespace} port-forward svc/myminio-console 9090:9090`
* `kubectl --namespace ${namespace} port-forward svc/dremio-client 9047:9047`
* `kubectl --namespace ${namespace} port-forward svc/${release-name}-worker 8080:8080`

## Access & Configure Dremio
* Once port-forward is done. Dremio UI will be able to access in url `http://localhost:9047`
* This will prompt to create admin user. Set up user.
* Adding Hive Meta Store
    * To add Hive meta store as source. More details refer (here)[https://docs.dremio.com/current/sonar/data-sources/metastores/hive/]
    * Click on `Add Data Soruce`
    * Select Hive3
    * Provide a name
    * Hive Metastore Host put `${release-name}-hive-metastore.${namespace}.svc.cluster.local`
    * Click save

## Deploying DAGs to Airflow
* DAGs can be deployed to airflow via Docker Image.
* Docker image should be build and tagged using minikube. To make it available inside minikube docker registry.
### Building Docker Image with Airflow DAGs
* Change directory to `./orchestration`
* Write DAGs under `dags` folder.
* Build the image using minikube and push to minikube docker registry with teh command `minikube build image -t ${repository}:${tag} .`
* Update the Image repository and tag in the root `play-ground-chart/values.yaml` file of the helm chart. Via the following values keys.
```yaml
defaultAirflowRepository: ${repository}
defaultAirflowTag: "${imageTag}"
airflowVersion: "${airflow-version}"
```
* Once this is done uninstall & install the helm chart again. Now DAGs will appear in airflow.

# Things to do
* Create job for hive metastore creation
