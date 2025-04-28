
We write an example of ingress in kuberntes that works and i can test it

### Steps:

1.  Make sure you have an **Ingress Controller** (e.g., Nginx Ingress Controller) installed in your cluster.
	
		kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml

then switch to the namespace:

	kubectl config set-context --current --namespace=ingress-nginx
    
2.  Use the following YAML configuration for the Ingress resource.
    

##### Example YAML Files:

1.  **Deployment and Service for Application A:**
    

	
		apiVersion: apps/v1
		kind: Deployment
		metadata:
		  name: app-a
		spec:
		  replicas: 1
		  selector:
		    matchLabels:
		      app: app-a
		  template:
		    metadata:
		      labels:
		        app: app-a
		    spec:
		      containers:
		      - name: app-a
		        image: hashicorp/http-echo
		        args:
		        - "-text=Hello from App A"
		        ports:
		        - containerPort: 5678
		---
		apiVersion: v1
		kind: Service
		metadata:
		  name: app-a-service
		spec:
		  selector:
		    app: app-a
		  ports:
		  - protocol: TCP
		    port: 80
		    targetPort: 5678



2.  **Deployment and Service for Application B:**
    

		apiVersion: apps/v1
		kind: Deployment
		metadata:
		  name: app-b
		spec:
		  replicas: 1
		  selector:
		    matchLabels:
		      app: app-b
		  template:
		    metadata:
		      labels:
		        app: app-b
		    spec:
		      containers:
		      - name: app-b
		        image: hashicorp/http-echo
		        args:
		        - "-text=Hello from App B"
		        ports:
		        - containerPort: 5678
		---
		apiVersion: v1
		kind: Service
		metadata:
		  name: app-b-service
		spec:
		  selector:
		    app: app-b
		  ports:
		  - protocol: TCP
		    port: 80
		    targetPort: 5678



3.  **Ingress Resource:**
    

		apiVersion: networking.k8s.io/v1
		kind: Ingress
		metadata:
		  name: example-ingress
		  annotations:
		    nginx.ingress.kubernetes.io/rewrite-target: /
		spec:
		  rules:
		  - host: "myapp.local"
		    http:
		      paths:
		      - path: /app-a
		        pathType: Prefix
		        backend:
		          service:
		            name: app-a-service
		            port:
		              number: 80
		      - path: /app-b
		        pathType: Prefix
		        backend:
		          service:
		            name: app-b-service
		            port:
		              number: 80
              

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
