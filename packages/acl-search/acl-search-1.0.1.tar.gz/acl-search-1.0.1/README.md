# ACL-SEARCH

#### Description:    

acl-search is a Python 2 utility to search through an ACL file to find intersecting destination IPs and return the full term.

-----

## Usage:

```
usage: acl-search [-h] ip acl_file

Searches for an IP or intersecting CIDR in the destination block within an ACL
file and returns the full term.

positional arguments:
  ip          an IP address to search for
  acl_file    path to the ACL file to search in

optional arguments:
  -h, --help  show this help message and exit
```


#### Setup + Simple Usage

1. `./setup.py install`
2. `./acl-search <IP_or_CIDR> <ACL_FILE>`

OR

`pip install acl-search`

** You can get help on the command line with `./acl-search -h`

#### There is also a Dockerfile:

1. `docker build -t aclsearch .`
2. `docker run -v $(pwd):/acl-search aclsearch acl-search <IP_or_CIDR> <ACL_FILE>`
(mounts your current directory so that you can pass the ACL_FILE into the utility)
