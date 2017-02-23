# devops-vibbo--libs

A compilation of python libraries intended to be reused in our projects

## Usage

Add in your requirements.txt

```
git+ssh://git@github.schibsted.io/scmspain/devops-vibbo--libs.git@master#aws
```

Install the libraries

```
pip install -r /path/to/requirements.txt
```

Import the libraries into your projects
 
```
from aws.cloudformation import Cloudformation
from aws.boto_connections import AWSBotoAdapter
```