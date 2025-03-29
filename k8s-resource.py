import os
import sys
import yaml

def generate_yaml(resource_kind):
    templates = {
        "pod": {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "example-pod"},
            "spec": {
                "containers": [{"name": "example-container", "image": "nginx"}]
            }
        },
        "deployment": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "example-deployment"},
            "spec": {
                "replicas": 2,
                "selector": {"matchLabels": {"app": "example"}},
                "template": {
                    "metadata": {"labels": {"app": "example"}},
                    "spec": {"containers": [{"name": "example-container", "image": "nginx"}]}
                }
            }
        },
        "statefulset": {
            "apiVersion": "apps/v1",
            "kind": "StatefulSet",
            "metadata": {"name": "example-statefulset"},
            "spec": {
                "serviceName": "example-service",
                "replicas": 2,
                "selector": {"matchLabels": {"app": "example"}},
                "template": {
                    "metadata": {"labels": {"app": "example"}},
                    "spec": {"containers": [{"name": "example-container", "image": "nginx", "volumeMounts": [{"name": "example-volume", "mountPath": "/data"}]}]}
                },
                "volumeClaimTemplates": [{
                    "metadata": {"name": "example-volume"},
                    "spec": {
                        "accessModes": ["ReadWriteOnce"],
                        "resources": {"requests": {"storage": "1Gi"}}
                    }
                }]
            }
        },
        "service": {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "example-service"},
            "spec": {
                "selector": {"app": "example"},
                "ports": [{"protocol": "TCP", "port": 80}],
                "type": "ClusterIP"
            }
        },
        "persistentvolume": {
            "apiVersion": "v1",
            "kind": "PersistentVolume",
            "metadata": {"name": "example-pv"},
            "spec": {
                "capacity": {"storage": "1Gi"},
                "accessModes": ["ReadWriteOnce"],
                "hostPath": {"path": "/mnt/data"}
            }
        },
        "persistentvolumeclaim": {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {"name": "example-pvc"},
            "spec": {
                "accessModes": ["ReadWriteOnce"],
                "resources": {"requests": {"storage": "1Gi"}}
            }
        },
        "configmap": {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "example-configmap"},
            "data": {"key": "value"}
        },
        "secret": {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {"name": "example-secret"},
            "type": "Opaque",
            "data": {"username": "dXNlcm5hbWU=", "password": "cGFzc3dvcmQ="}  # Base64 encoded
        },
        "ingress": {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {"name": "example-ingress"},
            "spec": {
                "rules": [{
                    "host": "example.com",
                    "http": {
                        "paths": [{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {"service": {"name": "example-service", "port": {"number": 80}}}
                        }]
                    }
                }]
            }
        },
        "job": {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {"name": "example-job"},
            "spec": {
                "template": {
                    "metadata": {"name": "example"},
                    "spec": {
                        "containers": [{"name": "example-container", "image": "busybox", "command": ["echo", "Hello Kubernetes!"]}],
                        "restartPolicy": "Never"
                    }
                }
            }
        },
        "cronjob": {
            "apiVersion": "batch/v1",
            "kind": "CronJob",
            "metadata": {"name": "example-cronjob"},
            "spec": {
                "schedule": "*/1 * * * *",
                "jobTemplate": {
                    "spec": {
                        "template": {
                            "spec": {
                                "containers": [{"name": "example-container", "image": "busybox", "command": ["echo", "Hello from CronJob!"]}],
                                "restartPolicy": "OnFailure"
                            }
                        }
                    }
                }
            }
        },
        "role": {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "Role",
            "metadata": {"namespace": "default", "name": "example-role"},
            "rules": [{"apiGroups": [""], "resources": ["pods"], "verbs": ["get", "list", "watch"]}]
        },
        "rolebinding": {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "RoleBinding",
            "metadata": {"namespace": "default", "name": "example-rolebinding"},
            "subjects": [{"kind": "User", "name": "example-user", "apiGroup": "rbac.authorization.k8s.io"}],
            "roleRef": {"kind": "Role", "name": "example-role", "apiGroup": "rbac.authorization.k8s.io"}
        }
    }

    if resource_kind.lower() not in templates:
        print(f"Resource kind '{resource_kind}' is not supported.")
        return

    yaml_content = templates[resource_kind.lower()]

    filename = f"{resource_kind.lower()}.yaml"
    with open(filename, 'w') as yaml_file:
        yaml.dump(yaml_content, yaml_file, default_flow_style=False)
        print(f"Generated {filename} for resource kind '{resource_kind}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python k8s-resource.py <resource-kind>")
        print("Supported resource kinds:")
        print(", ".join(["pod", "deployment", "statefulset", "service", "persistentvolume", 
                        "persistentvolumeclaim", "configmap", "secret", "ingress", 
                        "job", "cronjob", "role", "rolebinding"]))
        sys.exit(1)

    resource_kind = sys.argv[1]
    generate_yaml(resource_kind)
