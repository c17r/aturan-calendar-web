FROM c17r/py3-build AS build

ADD . /build/
WORKDIR /build/

RUN /venv/bin/pipenv install --dev \
&& /venv/bin/pipenv requirements > requirements.txt \
&& /venv/bin/pipenv run python setup.py bdist_wheel

FROM c17r/py3-webapp AS base

COPY --from=build /build/dist/*.whl /code/
ADD wsgi.py /code/
WORKDIR /code/

RUN /venv/bin/pip install --quiet --no-cache-dir /code/*.whl \
&& rm -f /code/*.whl

ENV \
UWSGI_WSGI_FILE=wsgi.py

CMD ["uwsgi"]
