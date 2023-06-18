FROM python:3.11-alpine as build-miniqc
RUN apk add git py3-build
COPY . /src
RUN pyproject-build /src

FROM python:3.11-alpine
COPY --from=build-miniqc /src/dist/*.whl .
RUN pip install --no-cache-dir $( ls *.whl ) \
    && rm -rf ~/.cache

ENTRYPOINT miniqc
