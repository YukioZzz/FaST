prefix=$(pwd)
kubectl delete sharepod --all -n faas-share-fn

kubectl delete pod  --grace-period=0 --force --all -n faas-share-fn

#kubectl delete pod --all  --grace-period=0 --force -n faas-share 

kubectl delete daemonset kubeshare-node-daemon -n kube-system

kubectl delete pod -l "kubeshare/role"="dummyPod" -n kube-system

kubectl delete pod kubeshare-device-manager -n kube-system

#kubectl delete pod kubeshare-scheduler  -n kube-system

#sudo rm -f /kubeshare/scheduler/podmanagerport/GPU-5dc0320f-f8ef-0fb7-7d48-98682d6d4837

#kubectl delete daemonset --all -n faas-share-fn

#kubectl delete deploy prometheus -n faas-share

#kubectl delete deploy gateway -n faas-share

#kubectl delete deploy --all  -n faas-share

#kubectl delete svc --all -n faas-share
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.12.2/nvidia-device-plugin.yml
cd go/src/github.com/Interstellarss/faas-share/
kubectl create -f namespaces.yml
kubectl create -f deploy/crd.yaml

kubectl get pod -A | grep node-daemon | awk '{print$2}' | xargs kubectl delete pod -n kube-system
kubectl get pod -A | grep nvidia-device | awk '{print$2}' | xargs kubectl delete pod -n kube-system

# Deploy mps and dcgm-exporter
 kubectl apply -f mps-test/mps-server-pod.yaml
cd $prefix && sudo cp -rf ./dcgm /etc/dcgm-exporter
kubectl apply -f dcgm/dcgm-exporter.yaml

helm repo update \
&& helm upgrade faas-share --debug --install faas-share/faas-share \
    --namespace faas-share  \
    --set functionNamespace=faas-share-fn \
    --set generateBasicAuth=false \
    --set kubeshareDeviceManager.image="yukiozhu/kubeshare-device-manager:v0.1.24-mps" \
    --set kubeshareNodeDaemon.geminiHookInit.image="yukiozhu/kubeshare-gemini-hook-init:mps" \
    --set kubeshareNodeDaemon.geminiScheduler.image="yukiozhu/kubeshare-gemini-scheduler:unlimit" \
    --set operator.image="yukiozhu/faas-share:v0.1.24-mps"

# Deploy Morphling
cd $prefix/morphling && chmod +x install.sh && ./install.sh

# Deploy autoscaler
cd $prefix/FaSTAutoscaler && make apply IMG=yukiozhu/fastautoscaler:latest
