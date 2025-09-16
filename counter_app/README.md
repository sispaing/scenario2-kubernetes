## check all contianers logs
``` bash
docker logs -f counter_app-backend-1
```

### Check the database
``` bash
docker compose exec mysql mysql -u root -p'rootpassword' -e 'SELECT value FROM counter_db.counter ORDER BY id DESC LIMIT 1;'

kubectl exec -it mysql-0 -n acp -- mysql -u root -p'rootpassword' -e 'SELECT value FROM counter_db.counter ORDER BY id DESC LIMIT 1;'
``

kubectl port-forward svc/frontend-service -n acp --address 0.0.0.0 8080:80

kubectl port-forward svc/frontend -n acp --address 0.0.0.0 8080:80

kubectl apply -f /home/vagrant/projects/acp_project/scenario2-kubernetes/counter_app/k8s

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
kubectl get pods -n monitoring
kubectl get svc -n monitoring
kubectl get pods -n monitoring
kubectl logs prometheus-grafana-74cf7d6768–77wms -c grafana -n monitoring
kubectl logs prometheus-grafana-5cd44bf8b9-hlgmx -c grafana -n monitoring
kubectl port-forward deployment/prometheus-grafana -n monitoring 0.0.0.0 3000:3000
kubectl port-forward deployment/prometheus-grafana -n monitoring 3000
kubectl port-forward deployment/prometheus-grafana -n monitoring --adredress 0.0.0.0.0 3000
kubectl port-forward deployment/prometheus-grafana -n monitoring --address 0.0.0.0. 3000
kubectl port-forward deployment/prometheus-grafana -n monitoring --address 0.0.0.0 3000
kubectl port-forward prometheus-prometheus-kube-prometheus-prometheus-0 9090 -n monitoring --address 0.0.0.0 