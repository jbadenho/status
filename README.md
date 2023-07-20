# docker-container-status
Shows the status of all docker containers on a server

## required apt packages

```bash
sudo apt install python3-venv python3-dev libsqlite3-dev
```

## starting the virtual enviroment

Need to run as root if testing from you local machine with the public an private ssh keys
```bash
sudo su
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### for development

```bash
flask --app main.py run --debug
```
### for production

```bash
uwsgi --ini uwsgi.ini --honour-stdin
```

## to deactivate venv

```bash
deactivate
```

```bash
rm -rf venv
```