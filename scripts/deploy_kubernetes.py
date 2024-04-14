# Installs K8s cluster on a remote machine
# 

import paramiko
import time

# SSH connection details
hostname = 'your_remote_machine_ip'
username = 'your_ssh_username'
password = 'your_ssh_password'

# Commands to install Kubernetes
commands = [
    'sudo apt-get update',
    'sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common',
    'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
    'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
    'sudo apt-get update',
    'sudo apt-get install -y docker-ce docker-ce-cli containerd.io',
    'sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -',
    'sudo cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list\n\
    deb https://apt.kubernetes.io/ kubernetes-xenial main\n\
    EOF',
    'sudo apt-get update',
    'sudo apt-get install -y kubelet kubeadm kubectl',
    'sudo swapoff -a',  # Disable swap to prevent kubelet startup errors
]

# Command to initialize Kubernetes master node
init_command = 'sudo kubeadm init --apiserver-advertise-address={0} --pod-network-cidr=192.168.0.0/16'.format(hostname)

# Command to join worker node to the cluster
join_command = 'sudo kubeadm join <master_ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>'

# Function to execute commands on the remote machine via SSH
def execute_commands(hostname, username, password, commands):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)

    for command in commands:
        print(f"Executing command: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        time.sleep(1)  # Add a small delay to ensure proper execution
        print(stdout.read().decode('utf-8'))

    ssh_client.close()

# Execute commands to install Kubernetes
execute_commands(hostname, username, password, commands)

# Execute command to initialize master node
execute_commands(hostname, username, password, [init_command])

# Execute command to join worker node to the cluster
execute_commands(hostname, username, password, [join_command])
