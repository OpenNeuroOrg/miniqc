FROM python:3.11-slim as build-miniqc
RUN pip install build
RUN apt-get update && apt-get install -y --no-install-recommends git
COPY . /src
RUN python -m build /src

FROM python:3.11-alpine
COPY --from=build-miniqc /src/dist/*.whl .
RUN pip install --extra-index-url https://alpine-wheels.github.io/index --no-cache-dir $( ls *.whl ) \
    && rm -rf ~/.cache

ENTRYPOINT miniqc
