from collections import UserDict


class K8sObject(UserDict):
    def dump(self):
        return dict(self)


class Deployment(K8sObject):
    ...
