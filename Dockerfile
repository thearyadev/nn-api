FROM python:3.11-slim-buster

LABEL org.opencontainers.image.source=https://github.com/thearyadev/nn-api
LABEL org.opencontainers.image.description="Docker image for nn-api"
LABEL org.opencontainers.image.licenses=MIT

WORKDIR /APP
COPY . /APP
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /root/.local/bin/poetry install
RUN cat checkpoint/chunk_* > checkpoint2.onnx
RUN mkdir ~/.NudeNet
RUN mv checkpoint2.onnx ~/.NudeNet/detector_v2_default_checkpoint.onnx
RUN mv classes ~/.NudeNet/classes


ENTRYPOINT [ "/root/.local/bin/poetry", "run", "uvicorn", "main:app", "--port", "8888", "--host", "0.0.0.0" ]