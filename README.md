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
* kubectl port-forward svc/minio-hl 9000 -n minio
