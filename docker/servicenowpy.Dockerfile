FROM python

COPY ./servicenowpy/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /servicenowpy

COPY ./servicenowpy .