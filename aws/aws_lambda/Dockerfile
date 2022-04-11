FROM amazon/aws-lambda-python:3.8

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

RUN yum install git -y

RUN git clone https://github.com/sktkddn777/lambda-with-docker-container.git

RUN pip install -r lambda-with-docker-container/requirements.txt

RUN cp -r lambda-with-docker-container/* /var/task

CMD ["lambda_function.handler"]