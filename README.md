# stealthizer/anthill

A compilation of python libraries intended to be reused in your projects

## Usage

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