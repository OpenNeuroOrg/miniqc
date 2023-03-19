FROM python:3.11-slim as build-miniqc
RUN pip install build
RUN apt-get update && apt-get install -y --no-install-recommends git
COPY . /src
RUN python -m build /src

FROM python:3.11-slim
COPY --from=build-miniqc /src/dist/*.whl .
RUN pip install --no-cache-dir $( ls *.whl ) \
    && rm -rf ~/.cache

ENTRYPOINT miniqc
