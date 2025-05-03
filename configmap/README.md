	export k="kubectl"
	
###  📌 **Step 1: Create a ConfigMap**

Create a **ConfigMap** named `my-config` with key-value pairs.

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  DATABASE_URL: "mysql://localhost:3306"
  APP_ENV: "production"
  custom.conf: |
    server {
      listen 80;
      server_name myapp.local;
      location / {
        root /usr/share/nginx/html;
      }
    }
```

Apply the ConfigMap:

```
kubectl apply -f my-configmap.yaml
```

### 📌 **Step 2: Use ConfigMap in a Pod**

Now, let's create a **Pod** that utilizes `my-config`:

```
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
  - name: my-container
    image: nginx
    env:
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: my-config
          key: DATABASE_URL
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: my-config
          key: APP_ENV
    volumeMounts:
    - name: config-volume
      mountPath: "/etc/nginx/conf.d"
  volumes:
  - name: config-volume
    configMap:
      name: my-config
      items:
      - key: custom.conf
        path: custom.conf
```

Apply the Pod:

```
kubectl apply -f my-app.yaml
```

### 🔥 **How Does This Work?**

✅ **Environment Variables** → The Pod will have `DATABASE_URL` and `APP_ENV` set from `my-config`. ✅ **Mounted Files** → The `custom.conf` file will be available in `/etc/nginx/conf.d/`.

### 📌 **Step 3: Verify the ConfigMap Usage**

Run the following command inside the Pod to check the environment variables:

	kubectl exec my-app -- printenv | grep DATABASE_URL
	kubectl exec my-app -- printenv | grep APP_ENV
Check if the **ConfigMap file** is mounted correctly:

	kubectl exec my-app -- cat /etc/nginx/conf.d/custom.conf