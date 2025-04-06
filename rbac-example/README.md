
Activating **Role-Based Access Control (RBAC)** in Kubernetes is essential for managing permissions securely. Here’s how you can enable and configure RBAC in your cluster:

### **Step 1: Ensure RBAC is Enabled**

RBAC is **enabled by default** on Kubernetes **v1.6+**, but you can confirm by checking the API server flags:

-   Run the following command on your **control plane node**:
    

    
    ```
    ps aux | grep kube-apiserver
    ```
    
-   Ensure the following flag exists:
    
    ```
    --authorization-mode=RBAC    
    ```
    

If RBAC is not enabled, modify your API server config:

-   For **kubeadm-based clusters**, edit:
    
      
    ```
    sudo nano /etc/kubernetes/manifests/kube-apiserver.yaml    
    ```
    
-   Add:
    
    
    
    ```
    - --authorization-mode=RBAC    
    ```
    
-   Restart the API server:
    
       
    ```
    sudo systemctl restart kubelet    
    ```
    

### **Step 2: Create a Role**

Define a **Role** that grants specific permissions within a namespace. Example:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: default
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

Apply the role:

```
kubectl apply -f pod-reader-role.yaml
```

### **Step 3: Create a RoleBinding**

To assign the Role to a specific user or service account:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: example-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io

```

Apply the RoleBinding:

```
kubectl apply -f role-binding.yaml
```

### **Step 4: Verify RBAC Permissions**

Use `kubectl auth can-i` to check permissions:

```
kubectl auth can-i list pods --as=example-user
```

If it returns `yes`, RBAC is correctly configured.

### **Step 5: Extend RBAC for Cluster-Wide Permissions (Optional)**

If you need cluster-wide permissions, use **ClusterRole** instead:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]

```

Apply:

```
kubectl apply -f cluster-role.yaml
```

This enables **RBAC authentication**, defines permissions, and assigns roles properly. Let me know if you need further customization!