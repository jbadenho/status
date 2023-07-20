from flask import Flask, render_template
import paramiko

app = Flask(__name__)

# Function to check container statuses and retrieve server name over SSH
def check_container_status():
    # SSH credentials for the remote server
    ssh_username = 'root'
    ssh_password = ''
    ssh_private_key_path = '/root/.ssh/id_rsa'
    ssh_port = 22  # SSH port (default: 22)
    remote_ip = '178.62.116.162'  # Hardcoded IP address of the server

    # Command to check Docker container status
    docker_command = 'docker ps -a --format "{{.Names}} - {{.Status}}"'

    # Create an SSH key object from the private key file
    private_key = None
    if ssh_private_key_path:
        private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_path)

    # Establish an SSH connection to the remote server
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # If using public key authentication
    if private_key:
        ssh_client.connect(remote_ip, port=ssh_port, username=ssh_username, pkey=private_key)
    # If using password authentication
    else:
        ssh_client.connect(remote_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    # Execute the Docker command on the remote server
    _, stdout, _ = ssh_client.exec_command(docker_command)
    docker_output = stdout.read().decode().strip()

    # Close the SSH connection
    ssh_client.close()

    # Parse the Docker output to get container status
    container_lines = docker_output.split('\n')
    containers = [line for line in container_lines]

    # Retrieve the server name
    server_name = get_server_name()

    return containers, server_name

# Function to retrieve the server name
def get_server_name():
    # SSH credentials for the remote server
    ssh_username = 'root'
    ssh_password = ''
    ssh_private_key_path = '/root/.ssh/id_rsa'
    ssh_port = 22  # SSH port (default: 22)
    remote_ip = '178.62.116.162'  # Hardcoded IP address of the server

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
        ssh_client.connect(remote_ip, port=ssh_port, username=ssh_username, pkey=private_key)
    # If using password authentication
    else:
        ssh_client.connect(remote_ip, port=ssh_port, username=ssh_username, password=ssh_password)

    # Execute the server name command on the remote server
    _, stdout, _ = ssh_client.exec_command(server_name_command)
    server_name = stdout.read().decode().strip()

    # Close the SSH connection
    ssh_client.close()

    return server_name

# Route to render the main page with the container status and server name
@app.route('/')
def home():
    containers, server_name = check_container_status()
    container_data = []

    if containers:
        for container in containers:
            container_info = container.split(' - ')
            if len(container_info) == 2:
                container_data.append(container_info)

    return render_template('index.html', containers=container_data, server_name=server_name)

def create_app():
   return app.run()

if __name__ == '__main__':
    #from waitress import serve
    #serve(app, host="127.0.0.1", port=5000)
    #serve(app.run(), host="0.0.0.0", port=8080)
    app.run()
