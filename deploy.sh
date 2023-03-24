# prerequisite
## install k6:
wget https://github.com/grafana/k6/releases/download/v0.43.1/k6-v0.43.1-linux-amd64.deb
sudo dpkg -i ./k6-v0.43.1-linux-amd64.deb

## install helm:
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

# prepare namespace 
kubectl apply -f faas-share/deploy/crd.yaml
kubectl apply -f https://raw.githubusercontent.com/Interstellarss/faas-share/master/namespaces.yml 
helm repo add faas-share  https://interstellarss.github.io/faas-share-charts/

bash ./reloadShare.sh
