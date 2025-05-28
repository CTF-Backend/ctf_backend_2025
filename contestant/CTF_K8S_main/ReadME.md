Install K3S In Your cluster With These Commands:

Install:
```
curl -sfL https://get.k3s.io | sh -
```

Check K3S Process Status:
```
sudo systemctl status k3s
```

Get Installed K3S Version:
```
k3s --version
```

Config `kubectl` Command To Use K3S:
```
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chmod 600 ~/.kube/config
```

Test It:
```
kubectl get nodes
```

Create A Pull Secret For Image Pulling With This Command:
```
kubectl create secret docker-registry hamravesh-registery \
  --docker-server=registry.hamdocker.ir/the-atid \
  --docker-username=the-atid \
  --docker-password=password
```

And Run The Program:
```
python3 main.py
```