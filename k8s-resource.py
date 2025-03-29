import sys
from typing import Dict

def generate_yaml(resource_type: str) -> str:
    """Generate basic YAML template for the specified Kubernetes resource type."""
    templates: Dict[str, str] = {
        "pod": """apiVersion: v1
kind: Pod
metadata:
  name: {name}
  labels:
    app: {name}
spec:
  containers:
  - name: {name}-container
    image: nginx
    ports:
    - containerPort: 80
""",
        "service": """apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  selector:
    app: {name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
""",
        "namespace": """apiVersion: v1
kind: Namespace
metadata:
  name: {name}
""",
        "deployment": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: nginx
        ports:
        - containerPort: 80
""",
        "statefulset": """apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {name}
spec:
  serviceName: "{name}-service"
  replicas: 3
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: nginx
        ports:
        - containerPort: 80
""",
        "daemonset": """apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: {name}
spec:
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: nginx
        ports:
        - containerPort: 80
""",
        "replicaset": """apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: {name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: nginx
        ports:
        - containerPort: 80
""",
        "job": """apiVersion: batch/v1
kind: Job
metadata:
  name: {name}
spec:
  template:
    spec:
      containers:
      - name: {name}-container
        image: busybox
        command: ["echo", "Hello Kubernetes!"]
      restartPolicy: Never
""",
        "cronjob": """apiVersion: batch/v1
kind: CronJob
metadata:
  name: {name}
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: {name}-container
            image: busybox
            command: ["echo", "Hello Kubernetes!"]
          restartPolicy: OnFailure
""",
        "ingress": """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {name}
spec:
  rules:
  - host: {name}.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {name}-service
            port:
              number: 80
""",
        "networkpolicy": """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {name}
spec:
  podSelector:
    matchLabels:
      app: {name}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: {name}-client
    ports:
    - protocol: TCP
      port: 80
""",
        "persistentvolume": """apiVersion: v1
kind: PersistentVolume
metadata:
  name: {name}
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: "/mnt/data"
""",
        "persistentvolumeclaim": """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {name}
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
""",
        "storageclass": """apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: {name}
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
""",
        "configmap": """apiVersion: v1
kind: ConfigMap
metadata:
  name: {name}
data:
  example.property.1: hello
  example.property.2: world
  example.property.file: |-
    property.1=value-1
    property.2=value-2    
""",
        "secret": """apiVersion: v1
kind: Secret
metadata:
  name: {name}
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
""",
        "node": """apiVersion: v1
kind: Node
metadata:
  name: {name}
  labels:
    node-role.kubernetes.io/worker: ""
""",
        "role": """apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {name}
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
""",
        "clusterrole": """apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: {name}
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
""",
        "rolebinding": """apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {name}
subjects:
- kind: User
  name: example-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: {name}
  apiGroup: rbac.authorization.k8s.io
""",
        "clusterrolebinding": """apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: {name}
subjects:
- kind: User
  name: example-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: {name}
  apiGroup: rbac.authorization.k8s.io
"""
    }

    resource_type = resource_type.lower()
    if resource_type not in templates:
        valid_resources = ", ".join(templates.keys())
        raise ValueError(f"Invalid resource type. Valid options are: {valid_resources}")

    return templates[resource_type]

def main():
    if len(sys.argv) != 2:
        print("Usage: python k8s-resource.py <resource-type>")
        print("Example: python k8s-resource.py deployment")
        sys.exit(1)

    resource_type = sys.argv[1].lower()
    resource_name = "example-" + resource_type

    try:
        yaml_template = generate_yaml(resource_type)
        formatted_yaml = yaml_template.format(name=resource_name)
        
        filename = f"{resource_name}.yaml"
        with open(filename, 'w') as f:
            f.write(formatted_yaml)
        
        print(f"Successfully generated {filename}")
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()