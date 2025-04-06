
## How to Use This Script

1.  Save the script as  `k8s-resource.py`
    
2.  Run it with a Kubernetes resource type as an argument, for example:

		python k8s-resource.py deployment
3.  The script will generate a YAML file named  `example-<resource-type>.yaml`  in the current directory

## Features

-   Supports all the resource types you requested:
    
    -   Core Resources: Pod, Service, Namespace, Node
        
    -   Workloads: Deployment, StatefulSet, DaemonSet, ReplicaSet, Job, CronJob
        
    -   Networking: Ingress, NetworkPolicy
        
    -   Storage: PersistentVolume (PV), PersistentVolumeClaim (PVC), StorageClass
        
    -   Configuration: ConfigMap, Secret
        
    -   RBAC: ClusterRole, Role, RoleBinding, ClusterRoleBinding
        
-   Each template includes the essential fields for the resource type
    
-   The generated YAML uses a standard naming convention (`example-<resource-type>`)
    
-   Includes error handling for invalid resource types

Here's the complete list of Kubernetes resource kinds that the script can generate YAML files for:

### Core Resources:

1.  **Pod**  - Basic workload unit in Kubernetes
    
2.  **Service**  - Network endpoint for pods
    
3.  **Namespace**  - Logical cluster partition
    
4.  **Node**  - Worker machine in Kubernetes
    

### Workload Resources:

5.  **Deployment**  - Declarative updates for Pods and ReplicaSets
    
6.  **StatefulSet**  - Manages stateful applications
    
7.  **DaemonSet**  - Ensures all nodes run a copy of a Pod
    
8.  **ReplicaSet**  - Maintains a stable set of replica Pods
    
9.  **Job**  - Creates one or more Pods that run to completion
    
10.  **CronJob**  - Runs Jobs on a time-based schedule
    

### Networking Resources:

11.  **Ingress**  - Manages external access to services
    
12.  **NetworkPolicy**  - Specifies how pods communicate
    

### Storage Resources:

13.  **PersistentVolume (PV)**  - Storage resource in the cluster
    
14.  **PersistentVolumeClaim (PVC)**  - User's storage request
    
15.  **StorageClass**  - Defines storage "classes" with different QoS levels
    

### Configuration Resources:

16.  **ConfigMap**  - Configuration data in key-value pairs
    
17.  **Secret**  - Sensitive configuration data
    

### RBAC Resources:

18.  **Role**  - Namespaced permissions rules
    
19.  **ClusterRole**  - Cluster-wide permissions rules
    
20.  **RoleBinding**  - Grants permissions within a namespace
    
21.  **ClusterRoleBinding**  - Grants cluster-wide permissions
    

To generate any of these, run the script with the resource kind in lowercase:

	python k8s-resource.py <resource-kind>

For example:

	python k8s-resource.py deployment
	python k8s-resource.py ingress
	python k8s-resource.py secret
