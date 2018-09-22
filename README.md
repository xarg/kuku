# kuku

[![Build Status](https://travis-ci.org/xarg/kuku.svg?branch=master)](https://travis-ci.org/xarg/kuku)

kuku generates kubernetes yaml manifests using python templates. It is similar to [helm](https://helm.sh/) in usage (templates dir, value files, etc..).


## Installation:

    pip install kuku

## Usage

Suppose you want to create a k8s service using a template where you define the service `name`, `internalPort` and `externalPort`.

Given the following `service.py` template:

```python
from kubernetes import client


def template(context):
    return client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(name=context["name"]),
        spec=client.V1ServiceSpec(
            type="NodePort",
            ports=[
                {"port": context["externalPort"], "targetPort": context["internalPort"]}
            ],
            selector={"app": context["name"]},
        ),
    )
```

You can now generate a yaml output from the above template using `kuku` by running: 

    $ ls .
    service.py 
    $ kuku generate -s name=kuku-web,internalPort=80,externalPort=80 .
    # Source: service.py
    apiVersion: v1
    kind: Service
    metadata:
      name: kuku-web
    spec:
      ports:
      - port: 80
        targetPort: 80
      selector:
        app: kuku-web
      type: NodePort
      
      
You can also combine the above with `kubectl apply -f -` to actually create your service on k8s:

    $ kuku generate -s name=kuku-web,internalPort=80,externalPort=80 . | kubectl apply -f -
    
Same as above, but let's make it shorter:

    $ kuku apply -s name=kuku-web,internalPort=80,externalPort=80 .
   
Finally to delete it: 

    $ kuku delete -s name=kuku-web,internalPort=80,externalPort=80 .
    
    # same thing as above
    
    $ kuku generate -s name=kuku-web,internalPort=80,externalPort=80 . | kubectl delete -f - 

## Templates      

Templates are python files that are defining a function called `template` that accepts a dict argument `context` and 
returns a k8s object or a list of k8s objects:

    def template(context):
        return V1Namespace(name=context['namespace'])  # example k8s object 

You can create multiple template files each defining their own `template` function.
`kuku` uses the k8s objects (aka models) from [official kubernetes python client package](https://github.com/kubernetes-client/python).
You can find them all [here](https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md#documentation-for-models)


## CLI

Similar to [helm](https://helm.sh/) `kuku` accepts defining it's context variables from the CLI:

    kuku -s namespace=kuku .
    
`-s namespace=kuku` will be passed to the `context` argument in your `template` function. Run `kuku -h` to find out more.

## Goals

#### Write python code to generate k8s manifests.
Python is a very popular language with a huge ecosystem of devops packages. Most importantly it's easier to debug than 
some templating languages used today to generate k8s manifests.

#### No k8s server side dependencies (i.e. tiller).
k8s already has a database for it's current state (using etcd). We can connect directly to it from the client to 
do our operations instead of relying on an extra server side dependency.

#### Local validation of manifests before running `kubectl apply`. 
Where possible do the validation locally using the [official k8s python client](https://github.com/kubernetes-client/python).

#### Use standard tools
Where possible use `kubectl` to apply changes to the k8s cluster instead of implementing a specific protocol.
Again, this will make debugging easier for the end user.

## Why not helm?

At [Gorgias](https://gorgias.io) we use [helm](https://helm.sh/) to manage our infrastructure, but there are a few 
things that we found problematic with it:

- Poor templating language: requires constant referral to the docs, whitespace issues, yaml formatting is hard.
- Server side dependency: if you upgrade the server -> every user needs to update their client - waste of valuable time.
- Lack of local validation: `helm lint` does not really ensure the validity (i.e. required keys for a k8s object) of the manifest.

Chart names, releases and other helm specific features do not really fit with our current workflow.


# Contributing

Contributions (code, issues, docs, etc..) are welcome!

Once you have your python environment setup:

    pip install -e .[dev] # will install dev dependencies
    pre-commit install # will install pre-commit hooks for code quality checking 
    
Publish a new version to pypi:

    python setup.py upload
