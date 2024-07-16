FROM ubuntu:22.04
LABEL authors="Joshua"

ENV TZ=America/Chicago
ENV SHELL /bin/bash
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies and tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y sudo curl git python3 python3-pip mysql-server pkg-config && \
    apt-get install -y libmysqlclient-dev libssl-dev libffi-dev && \
    apt-get clean

# Ensure MySQL can run as a service
RUN mkdir -p /var/run/mysqld && chown -R mysql:mysql /var/run/mysqld

# Install pip packages
RUN pip3 install mysqlclient flasgger flask flask-cors flask-restful flask-sqlalchemy requests

# set working dir

WORKDIR /usr/src/app

# Copy application
COPY . .



# Expose the MySQL port
EXPOSE 3306
EXPOSE 5000
EXPOSE 5001

# AirBnB Clone Environment Variables
ENV HBNB_MYSQL_USER=hbnb_dev
ENV HBNB_MYSQL_PWD=hbnb_dev_pwd
ENV HBNB_MYSQL_HOST=localhost
ENV HBNB_MYSQL_DB=hbnb_dev_db
ENV HBNB_TYPE_STORAGE=db

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


# Set the default command to keep the container running
CMD ["tail", "-f", "/dev/null"]