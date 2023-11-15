## [FaST-GShare:  Enabling Efficient Spatio-Temporal GPU Sharing in Serverless Computing for Deep Learning Inference](https://dl.acm.org/doi/10.1145/3605573.3605638) 

Authors: Jianfeng Gu, Yichao Zhu, Puxuan Wang, Mohak Chadha, Michael Gerndt

#### Base Infrastructure Configuraiton and Deployment:
- Install CUDA Driver. (both Master and Node)
```
sudo apt-get update
sudo apt-get install -y nvidia-driver-525
nvidia-smi
## if has problem, reboot the server
sudo reboot
```

- Install CUDA toolkit (both Master and Node)
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

- Install Kubernetes (Node)
```
bash install_k8s_node.sh
```
Then join the master node after install nvidia-container-toolkit shown below
```
# check the join command
kubeadm token create --print-join-command
# follow the command prompted and join the node to the master node
kubeadm join <ip:port> --token <the_join_token>
```



- Install/configure nvidia-container-toolkit (both Master and Node)
```
bash install_nvidia_container_toolkit.sh
```

- Install and deploy nvidia-device-plugin: (only the Master)
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


### Publication
If you use FaST-GShare, please cite us:
```
@inproceedings{gu2023fast,
  title={FaST-GShare: Enabling Efficient Spatio-Temporal GPU Sharing in Serverless Computing for Deep Learning Inference},
  author={Gu, Jianfeng and Zhu, Yichao and Wang, Puxuan and Chadha, Mohak and Gerndt, Michael},
  booktitle={Proceedings of the 52nd International Conference on Parallel Processing},
  pages={635--644},
  year={2023}
}
```

