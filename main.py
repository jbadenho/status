# main.py
from flask import Flask, render_template
import paramiko

app = Flask(__name__)

# Function to establish an SSH connection to the remote server
def establish_ssh_connection(server_ip, ssh_username, ssh_password, ssh_private_key_path):
    ssh_port = 22  # SSH port (default: 22)

    # Create an SSH key object from the private key file
    private_key = None
    if ssh_private_key_path:
        private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_path)

    # Establish an SSH connection to the remote server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # If using public key authentication
    if private_key:
        ssh_client.connect(server_ip, port=ssh_port, username=ssh_username, pkey=private_key)
    # If using password authentication
    else:
        ssh_client.connect(server_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    return ssh_client

# Function to check container statuses and retrieve server name over SSH
def check_container_status(server_ip, ssh_username, ssh_password, ssh_private_key_path):
    try:
        # SSH credentials for the remote server

        # Command to check Docker container status
        docker_command = 'docker ps -a --format "{{.Names}} - {{.Status}}"'

        # Establish an SSH connection to the remote server
        ssh_client = establish_ssh_connection(server_ip, ssh_username, ssh_password, ssh_private_key_path)

        # Execute the Docker command on the remote server
        _, stdout, _ = ssh_client.exec_command(docker_command)
        docker_output = stdout.read().decode().strip()

        # Close the SSH connection
        ssh_client.close()

        # Parse the Docker output to get container status
        container_lines = docker_output.split('\n')
        containers = [line for line in container_lines]

        # Retrieve the server name
        server_name = get_server_name(server_ip, ssh_username, ssh_password, ssh_private_key_path)

        return containers, server_name

    except paramiko.AuthenticationException:
        return [], "Authentication Failed"
    except paramiko.SSHException as ssh_ex:
        return [], f"SSH Error: {str(ssh_ex)}"
    except Exception as ex:
        return [], f"Error: {str(ex)}"

# Function to retrieve the server name
def get_server_name(server_ip, ssh_username, ssh_password, ssh_private_key_path):
    # SSH credentials for the remote server
    ssh_username = 'root'
    ssh_password = ''
    ssh_private_key_path = '/root/.ssh/id_rsa'
    ssh_port = 22  # SSH port (default: 22)

    # Command to retrieve the server name
    server_name_command = 'hostname'

    # Create an SSH key object from the private key file
    private_key = None
    if ssh_private_key_path:
        private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_path)

    # Establish an SSH connection to the remote server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # If using public key authentication
    if private_key:
        ssh_client.connect(server_ip, port=ssh_port, username=ssh_username, pkey=private_key)
    # If using password authentication
    else:
        ssh_client.connect(server_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    # Execute the server name command on the remote server
    _, stdout, _ = ssh_client.exec_command(server_name_command)
    server_name = stdout.read().decode().strip()

    # Close the SSH connection
    ssh_client.close()

    return server_name

# Function to read server IPs from the file
def get_server_ip():
    with open('database/server_ips.txt', 'r') as file:
        server_ip = file.read().splitlines()
    return server_ip

# Function to check if all containers for a server are green (up/healthy)
def are_all_containers_green(containers):
    for container_info in containers:
        container_status = container_info[1].lower()
        if 'Up' not in container_status and 'healthy' not in container_status:
            return False
    return True

# Route to render the main page with the container status and server name
@app.route('/')
def home():
    server_ip = get_server_ip()
    server_containers = {}
    summary_server_containers = {}
    all_green = True  # Flag to check if all containers are green

    for server_ip in server_ip:
        containers, server_name = check_container_status(server_ip, ssh_username='root', ssh_password='', ssh_private_key_path='/root/.ssh/id_rsa')

        container_data = []
        if containers:
            for container in containers:
                container_info = container.split(' - ')
                if len(container_info) == 2:
                    container_data.append(container_info)
        else:
            container_data.append(('No Containers', 'No Containers'))

        server_containers[server_name] = container_data

        # Check if any container is red (down/ unhealthy)
        if are_all_containers_green(container_data):
            all_green = True

    # Add the "Summary" tab based on container statuses
    summary_status = "All Good" if all_green else "Some Containers Are Down"
    summary_status_color = "All Good" if all_green else "Some Containers Are Down"
    summary_server_containers["Summary"] = [(summary_status, summary_status_color)]

    # Print the value of all_green on the server-side
    print("all_green:", all_green)

    return render_template('index.html', server_containers=server_containers, summary_server_containers=summary_server_containers, all_green=all_green)

if __name__ == '__main__':
    app.run()
