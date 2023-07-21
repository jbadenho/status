import paramiko

def test_ssh_connection(host, port, username, password=None, private_key_path=None):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if private_key_path:
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            ssh_client.connect(host, port=port, username=username, pkey=private_key)
        else:
            ssh_client.connect(host, port=port, username=username, password=password)

        print(f"Successfully connected to {host}:{port} via SSH.")
        ssh_client.close()
        return True

    except paramiko.AuthenticationException as e:
        print("Authentication failed:", str(e))
    except paramiko.SSHException as e:
        print("SSH connection failed:", str(e))
    except Exception as e:
        print("Error:", str(e))

    return False

if __name__ == "__main__":
    # Modify these variables with your server's information
    host = "178.62.116.162"
    port = 22
    username = "root"
    password = ""  # Only use password or private_key_path, not both
    private_key_path = None  # Set this to the path of your private key file if using key-based authentication

    test_ssh_connection(host, port, username, password, private_key_path)
