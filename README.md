# stealthizer/anthill

A compilation of python libraries intended to be reused in your projects

## Usage

You need to prepare your virtual environment first:

```bash
$ virtualenv --python=python3 venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Add in your requirements.txt

```
git+ssh://git@github.com/stealthizer/anthill.git@master#aws
```

Install the libraries

```bash
pip install -r /path/to/requirements.txt
```

Import the libraries into your projects
 
```python
from aws.cloudformation import Cloudformation
from aws.boto_connections import AWSBotoAdapter
```