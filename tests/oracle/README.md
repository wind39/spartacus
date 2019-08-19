#### Requirements

Download Oracle Linux 7 base image:

```
docker pull oraclelinux:7
```

For more information about Oracle Linux official docker images, please check here:

https://hub.docker.com/_/oraclelinux

Change into the directory:

```
cd spartacus/Spartacus/tests/oracle/
```

Download the installation rpm file from OTN into this folder - first time only:

https://www.oracle.com/technetwork/database/database-technologies/express-edition/downloads/index.html


#### Creating the test image

Create new test image:

```
docker build -t "spartacus:tests_oracle" .
```

After that you can delete the rpm file from this folder.


#### Starting the container

To test OmniDB, start a container from the test image, and a shell into the container:

```
docker run -it --rm -p 1521:1521 spartacus:tests_oracle /bin/bash
```

Inside the container, start the Oracle instance:

```
/etc/init.d/oracle-xe-18c start
```

Because of the `--rm` above, the container will be automatically destroyed when
you exit the container shell.


#### Connecting to Oracle

From OmniDB you can connect using these information:

- Host: 127.0.0.1
- Port: 1521
- Service: XE
- User: SYSTEM
- Password: spartacus

If you get this error:

```
ORA-24454: client host name is not set
```

Then on the client machine you need to do this (I needed to do this on Mac):

```
sudo /bin/bash -c "echo '127.0.1.1 ${HOSTNAME}' >> /etc/hosts"
```

You can create a non-system user like this (in the container, as `root`):

```
su oracle
sqlplus / as sysdba

alter session set "_ORACLE_SCRIPT"=true;
create user spartacus identified by spartacus;
grant dba to spartacus;
```


#### Inserting data into the database

In the `samples` folder there is a SQL script to create some tables and add some
data to Oracle. Decompress it and copy it to the running Oracle container:

```
gunzip dellstore2-oracle.sql.gz
docker cp dellstore2-oracle.sql <container_id>:/tmp/dellstore2-oracle.sql
```

Now inside the container, as `oracle` user, copy it to the home directory and
run the script:

```
cp /tmp/dellstore2-oracle.sql .
time sqlplus spartacus/spartacus@XE @dellstore2-oracle.sql
```


#### Running the tests (TODO)

To run the tests, outside of the container, execute:


#### Destroying the container

If you don't use `--rm` to create the container, you can destroy the container
anytime.

First you need to list the containers:

```
docker container ls
```

Then you can remove with:

```
docker container rm <container_id>
```


#### Destroying the image

You don't need to destroy the image, as it will be used for the next OmniDB
deployment.

To list all images:

```
docker images
```

You can destroy the image with:

```
docker image rm spartacus:tests_oracle
```
