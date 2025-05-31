FROM python:3.10-slim

RUN ln -snf /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && echo Asia/Ho_Chi_Minh > /etc/timezone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install libmagic1 zip wget -y 

# Install pip requirements
RUN python -m pip install pip setuptools wheel
COPY . /app
WORKDIR /app

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Install opencv dependencies
# CMD ["/bin/bash"]



EXPOSE 8000

RUN chmod -R +x scripts/
CMD ["sh", "scripts/run.sh"]