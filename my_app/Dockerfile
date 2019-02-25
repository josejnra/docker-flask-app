# image based on
FROM python:3.6

MAINTAINER "Jose Nunes"

# define working directory
WORKDIR /app

# copy my_app files to workdir
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

# Define ports that may be accessible
EXPOSE 5000

# define
ENTRYPOINT ["python"]

# which file to execute
CMD ["app.py"]
