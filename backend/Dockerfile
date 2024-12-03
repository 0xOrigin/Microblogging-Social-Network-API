FROM python:3.12.3-alpine AS development


# Set environment variables
ENV DockerHOME=/home/app/backend
ARG PORT

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p "$DockerHOME" && mkdir "$DockerHOME"/staticfiles && mkdir "$DockerHOME"/media

# Where your backend app lives in your docker container
WORKDIR $DockerHOME

# Install necessary packages on the container
RUN apk update && apk add --no-cache python3-dev postgresql-dev musl-dev build-base linux-headers gettext icu-data-full

# Copy the necessary files to the container
COPY requirements.txt $DockerHOME
COPY run.sh $DockerHOME

# Install any needed packages specified in requirements.txt and upgrade pip
RUN sh run.sh -s

# Make port available to the world outside this container
EXPOSE $PORT

# Run the application
CMD ["sh", "run.sh", "-t", "development"]


#######################################################################################

FROM python:3.12.3-alpine AS production


# Set environment variables
ENV DockerHOME=/home/app/backend
ARG PORT

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p "$DockerHOME" && mkdir "$DockerHOME"/staticfiles && mkdir "$DockerHOME"/media

# Where your backend app lives in your docker container
WORKDIR $DockerHOME

# Install necessary packages on the container
RUN apk update && apk add --no-cache python3-dev postgresql-dev musl-dev build-base linux-headers gettext icu-data-full

# Copy the necessary files to the container
COPY requirements.txt $DockerHOME
COPY run.sh $DockerHOME

# Install any needed packages specified in requirements.txt and upgrade pip
RUN sh run.sh -s

# Make port available to the world outside this container
EXPOSE $PORT

# Run the application
CMD ["sh", "run.sh", "-t", "production"]
