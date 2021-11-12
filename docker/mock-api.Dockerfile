FROM python

COPY ./mock_api/requirements.txt requirements.txt
RUN [ "pip3", "install", "-r", "requirements.txt" ]

WORKDIR /mock_api

COPY ./mock_api .

CMD [ "python3", "mock_api.py" ]