FROM python:3.6

LABEL name="kuku"
LABEL version="0.1"
LABEL description="Kubernetes templating tool"
LABEL maintainer="Alex Plugaru"

RUN pip install -U pip 

COPY . /src/
# kubernetes pypi package requires a ~./kube/config file so we're providing a dummy here 
RUN mkdir ~/.kube/ && cp /src/examples/kube-config ~/.kube/config
RUN cd /src/ && pip install -e .

ENTRYPOINT ["kuku"]
