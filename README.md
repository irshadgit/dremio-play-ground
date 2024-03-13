# dremio-play-ground
Repository for dremio-play-ground.

# Helm Install

* Add helm repo to install minio-operator
* helm repo add minio https://operator.min.io/
* helm install --namespace play-ground --create-namespace minio-operator minio/operator
* helm list --all-namespaces
* helm uninstall any-releases
* helm install --namespace play-ground --create-namespace play-ground ./play-ground-chart
* kubectl --namespace play-ground port-forward svc/myminio-console 9443:9443
* kubectl port-forward svc/myminio-hl 9000 -n minio


Issue encoutnered 
* https based access was failing. Disabled ssl for minio using helm chart.
Settings for spark accessing minio
    hadoopConf.set("fs.s3a.access.key", "minio")
    hadoopConf.set("fs.s3a.secret.key", "minio123")
    hadoopConf.set("fs.s3a.endpoint", "http://localhost:9443")
    hadoopConf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoopConf.set("fs.s3a.path.style.access", "true")
