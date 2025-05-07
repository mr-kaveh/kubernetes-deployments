## **Install and Enable Metrics Server**

HPA requires **Metrics Server** to gather CPU and memory data.

### **🛠 Install Metrics Server**

Apply the official **Metrics Server deployment**:



```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability.yaml
```

### **🔹 Verify Metrics Server is Running**

Check if Metrics Server is active:



```
kubectl get pods -n kube-system | grep metrics-server
```

Check if API is available:

```
kubectl get apiservices | grep metrics
```

## **2️⃣ Create a Sample Deployment**

You need a **Deployment** for HPA to scale.

### **🛠 Example Deployment (**`deployment.yaml`**)**

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app-container
        image: nginx
        resources:
          requests:
            cpu: "200m"
          limits:
            cpu: "500m"

```
and a **Service**

```
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP  # Use NodePort or LoadBalancer if external access is needed

```
Apply them:

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## **3️⃣ Create an HPA Based on CPU Utilization**

Now, set up **Horizontal Pod Autoscaler**.

### **🛠 HPA YAML File (**`hpa.yaml`**)**

```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply it:

```
kubectl apply -f hpa.yaml
```

## **4️⃣ Verify HPA is Working**

Check the HPA status:

```
kubectl get hpa my-app-hpa
```

Check pod scaling:

```
kubectl get pods -w
```

**Trigger scaling manually**:



```
kubectl run --rm -it load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://my-app-service.default.svc.cluster.local; done"
```