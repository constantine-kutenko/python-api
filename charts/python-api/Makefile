
#
#
#

CHART_NAME="python-api"
RELEASE_NAME="python-api"
NAMESPACE="default"

lint:
	@helm lint --strict

template:
	@helm template \
	--set tags.bare_metal=false \
	--set ingress.enabled=false \
	--set env.POSTGRESQL_DATABASE_NAME=passengers \
	--set env.POSTGRESQL_DATABASE_USER=titanic .

dryrun:
	@clear
	@helm install \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--dry-run \
		--debug \
		--name python-api-dryrun \
		--namespace test \
		--set location=local \
		--set ingress.enabled=false 
		--set env.POSTGRESQL_DATABASE_NAME=passengers \
		--set env.POSTGRESQL_DATABASE_USER=titanic .

install:
	@clear
	@helm delete --purge python-api; exit 0
	@#helm repo update
	@#helm dependency update python-api/python-api
	@helm install \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--name python-api \
		--namespace default \
		--set location=local \
		--set ingress.enabled=false \
		--set env.POSTGRESQL_DATABASE_NAME=passengers \
		--set env.POSTGRESQL_DATABASE_USER=titanic .
	@helm ls python-api


upgrade:
	@clear
	@helm ls python-api; echo -e "\n\n"
	@helm get values \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--all python-api > /tmp/python-api.values
	@#helm repo update
	@helm upgrade \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		python-api \
		-f /tmp/python-api.values \
		--set location=local \
	@rm -f /tmp/python-api.values
	@helm ls \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		python-api
