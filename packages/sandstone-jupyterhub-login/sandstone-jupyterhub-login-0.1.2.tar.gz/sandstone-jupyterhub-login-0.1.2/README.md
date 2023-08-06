# sandstone-jupyterhub-login
[![DOI](https://zenodo.org/badge/87221406.svg)](https://zenodo.org/badge/latestdoi/87221406)

Use JupyterHub as a multi-user spawner for Sandstone IDE

## Installation
Install the Python module to your Sandstone IDE environment first
```
python setup.py install
```

Then modify your Sandstone IDE configuration to use the Sandstone JupyterHub Login handler, and to pull the URL prefix from the environment.
```python
import os

LOGIN_HANDLER = 'sandstone_jupyterhub_login.handlers.JupyterHubLoginHandler'

URL_PREFIX = os.environ.get('SANDSTONE_PREFIX', '')
```

JupyterHub can now invoke Sandstone IDE by running
```
<sandstone-python-path>/bin/sandstone-jupyterhub
```

### Using self-signed certificates
If you have deployed JupyterHub over SSL using a self-signed certificate, then you must deconfigure verification in the login handler:
```python
VERIFY_JH_CERT = False
```
