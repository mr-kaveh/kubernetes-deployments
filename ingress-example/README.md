
Here's an example of a **Kubernetes Ingress** that you can test. It sets up an Ingress to route traffic to two different Services based on the URL path.

### Steps:

1.  Make sure you have an **Ingress Controller** (e.g., Nginx Ingress Controller) installed in your cluster.
	
		kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml

then switch to the namespace:

	kubectl config set-context --current --namespace=ingress-nginx

 ### Install MetalLB
	kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml

### Configure MetalLB

	apiVersion: metallb.io/v1beta1
	kind: IPAddressPool
	metadata:
	  name: my-ip-pool
	  namespace: metallb-system
	spec:
	  addresses:
	  - 192.168.1.100-192.168.1.110
	---
	apiVersion: metallb.io/v1beta1
	kind: L2Advertisement
	metadata:
	  name: l2-advertisement
	  namespace: metallb-system
    
2.  Use the following YAML configuration for the Ingress resource.
    

##### Example YAML Files:

1.  **Deployment and Service for Application A:**
    

	
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aks-helloworld-one  
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aks-helloworld-one
  template:
    metadata:
      labels:
        app: aks-helloworld-one
    spec:
      containers:
      - name: aks-helloworld-one
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80
        env:
        - name: TITLE
          value: "Welcome to Azure Kubernetes Service (AKS)"
---
apiVersion: v1
kind: Service
metadata:
  name: aks-helloworld-one  
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    app: aks-helloworld-one
```



2.  **Deployment and Service for Application B:**
    

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aks-helloworld-two  
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aks-helloworld-two
  template:
    metadata:
      labels:
        app: aks-helloworld-two
    spec:
      containers:
      - name: aks-helloworld-two
        image: mcr.microsoft.com/azuredocs/aks-helloworld:v1
        ports:
        - containerPort: 80
        env:
        - name: TITLE
          value: "AKS Ingress Demo"
---
apiVersion: v1
kind: Service
metadata:
  name: aks-helloworld-two  
spec:
  type: ClusterIP
  ports:
  - port: 80
  selector:
    app: aks-helloworld-two
```



3.  **Ingress Resource:**
    

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-world-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /hello-world-one(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: aks-helloworld-one
            port:
              number: 80
      - path: /hello-world-two(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: aks-helloworld-two
            port:
              number: 80
      - path: /(.*)
        pathType: Prefix
        backend:
          service:
            name: aks-helloworld-one
            port:
              number: 80
```
              




### How It Works:

-   Requests to `http://myapp.local/app-a` are routed to `app-a-service`, which responds with **"Hello from App A"**.
    
-   Requests to `http://myapp.local/app-b` are routed to `app-b-service`, which responds with **"Hello from App B"**.
    

### Testing:

1.  Apply the YAML files in order:
    
    bash
    
    ```
    kubectl apply -f app-a.yaml
    kubectl apply -f app-b.yaml
    kubectl apply -f ingress.yaml
    
    ```
    
2.  Update your `/etc/hosts` file to map `myapp.local` to your cluster's Ingress IP:
    
    bash
    
    ```
    <INGRESS_IP> myapp.local
    
    ```
    
3.  Test the paths:
    
    -   Open your browser or use `curl` to test:
        
        bash
        
        ```
        curl http://myapp.local/app-a
        curl http://myapp.local/app-b
        
        ```
        

If you encounter any issues, feel free to ask for debugging tips!
