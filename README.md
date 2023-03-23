## FaST: a FaaS oriented Spatio-Temporal Sharing Framework

Deployment:

- git clone git@github.com:YukioZzz/FaST.git
- git submodule init && git submodule update --recursive --remote
- ./reloadShare.sh
- apply test function: kubectl apply -f FaSTAutoscaler/config/samples/fastsvc_v1_fastsvc.yaml
- install k6
- load test: cd faas-share-test/MLPerf-based-workloads/resnet/client && k6 run k6.js (remember to edit gateway ip) 


Prerequisite:

install k6:
```
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6
```
install helm:
```
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```
