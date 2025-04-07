
### **1. Deploy Dex as an OIDC Provider**

Dex acts as an **identity provider** that bridges LDAP authentication with Kubernetes.

#### **Dex Configuration Example (**`dex-config.yaml`**)**
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: dex
  namespace: dex
data:
  config.yaml: |
    issuer: https://dex.example.com
    storage:
      type: memory
    connectors:
    - type: ldap
      id: ldap
      name: LDAP
      config:
        host: ldap.example.com:389
        insecureNoSSL: false
        bindDN: "cn=admin,dc=example,dc=com"
        bindPW: "admin-password"
        userSearch:
          baseDN: "dc=example,dc=com"
          filter: "(objectClass=person)"
          username: sAMAccountName
          idAttr: uid
          emailAttr: mail
          nameAttr: cn
```

-   **Dex connects to LDAP** and authenticates users.
    
-   Users log in via Dex, which validates credentials against LDAP.
    

Deploy Dex:

```
kubectl apply -f dex-config.yaml
```

### **2. Configure Kubernetes API Server for OIDC**

Modify the **kube-apiserver** configuration (`/etc/kubernetes/manifests/kube-apiserver.yaml`):

```
- --oidc-issuer-url=https://dex.example.com
- --oidc-client-id=kubernetes
- --oidc-username-claim=email
- --oidc-groups-claim=groups
- --oidc-ca-file=/etc/kubernetes/pki/ca.crt
```

Restart the API server:

```
sudo systemctl restart kubelet
```

### **3. Create RBAC Role for LDAP Users**

Define a **ClusterRoleBinding** to grant permissions to authenticated LDAP users:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ldap-user-binding
subjects:
- kind: User
  name: ldap-user@example.com  # Must match LDAP username
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

Apply the configuration:

```
kubectl apply -f ldap-role-binding.yaml
```

### **4. Authenticate Users via OIDC**

Once configured, users authenticate via **OIDC tokens** issued by Dex:

```
kubectl config set-credentials ldap-user --token=<OIDC-TOKEN>
```

Then, verify permissions:

```
kubectl auth can-i get pods --as=ldap-user@example.com
```

### **5. Verify Logs & Debug Issues**

Check logs to troubleshoot authentication issues:

```
kubectl logs -n kube-system kube-apiserver-<control-plane-node>
```

This setup enables **LDAP-based authentication** via **Dex and OIDC**, allowing users to securely log in to Kubernetes. You can find a detailed guide here. Let me know if you need help with a specific provider!