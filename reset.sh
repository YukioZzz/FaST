kubectl delete pe --all
bash ./reloadShare.sh
kubectl create -f ./morphling/experiment-bert-grid.yaml
