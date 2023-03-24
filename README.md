## FaST: a FaaS oriented Spatio-Temporal Sharing Framework

#### Base Infrastructure Configuraiton and Deployment:
- Install CUDA Driver
```
sudo apt-get update
sudo apt-get install -y nvidia-driver-525
nvidia-smi
## if has problem, reboot the server
sudo reboot
```

- Install CUDA toolkit
```
sudo apt install -y nvidia-cuda-toolkit
```

- Install Kubernetes (Master Node)
```
bash install_k8s_master_node.sh
```
check if the master node's is under untiant
```
kubectl describe node <node_name> | grep -i taint
```
if not untaint and the master node is also regard as a computing node, untiant the node
```
kubectl taint node `hostname` node-role.kubernetes.io/control-plane:NoSchedule-
kubectl taint node `hostname` node-role.kubernetes.io/master:NoSchedule-

```




- Install/configure nvidia-container-toolkit
```
bash install_nvidia_container_toolkit.sh
```

- Install and deploy nvidia-device-plugin:
```
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml
```

#### Deployment:

- clone repo:
```
git clone git@github.com:YukioZzz/FaST.git
```
- pull submodules:
```
git submodule init && git submodule update --recursive --remote
```
- install prerequisites and deploy components:
```
bash ./deploy.sh
```
- apply test function:
```
kubectl apply -f FaSTAutoscaler/config/samples/fastsvc_v1_fastsvc.yaml
```
- load test(remember to edit gateway ip):
```
cd faas-share-test/MLPerf-based-workloads/resnet/client && k6 run k6.js 
```

