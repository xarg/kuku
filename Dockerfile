FROM python:3.5

LABEL name="kuku"
LABEL version="0.0.5"
LABEL description="Kubernetes templating tool"
LABEL maintainer="Alex Plugaru"

RUN pip install -U pip

COPY . /src/
RUN cd /src/ && pip install -e .

ENTRYPOINT ["kuku"]
