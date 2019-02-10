
#
#
#

CHART_NAME="postgresql"
RELEASE_NAME="postgresql"
NAMESPACE="default"

lint:
	@helm lint --strict

template:
	@helm template .

dryrun:
	@clear
	@helm install \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--dry-run \
		--debug \
		--name postgresql-dryrun \
		--namespace test \
		--set location=local .

install:
	@clear
	@helm delete --purge postgresql; exit 0
	@#helm repo update
	@#helm dependency update postgresql/postgresql
	@helm install \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--name postgresql \
		--namespace default \
		--set location=local .
	@helm ls postgresql


upgrade:
	@clear
	@helm ls postgresql; echo -e "\n\n"
	@helm get values \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		--all postgresql > /tmp/postgresql.values
	@#helm repo update
	@helm upgrade \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		postgresql \
		-f /tmp/postgresql.values \
		--set location=local \
	@rm -f /tmp/postgresql.values
	@helm ls \
		--kube-context minikube \
		--tiller-namespace kube-system \
		--tiller-connection-timeout 15 \
		postgresql
