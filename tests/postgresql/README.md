#### Requirements

Download Debian 10 base image:

```
docker pull debian:stable-slim
```

For more information about Debian official docker images, please check here:

https://hub.docker.com/_/debian


#### Creating the test image

Create new test image:

```
docker build -t "spartacus:tests_postgresql" .
```


#### Starting the container

To test OmniDB, start a container from the test image, and a shell into the container:

```
docker run -it --rm -p 5494:5494 -p 5495:5495 -p 5496:5496 -p 5410:5410 -p 5411:5411 -p 5412:5412 spartacus:tests_postgresql /bin/bash
```

Inside the container, start all PostgreSQL instances:

```
pg_ctlcluster 9.4 main start
pg_ctlcluster 9.5 main start
pg_ctlcluster 9.6 main start
pg_ctlcluster 10 main start
pg_ctlcluster 11 main start
pg_ctlcluster 12 main start
```

Also inside the container, restore the sample database:

```
./restore.sh
```

Because of the `--rm` above, the container will be automatically destroyed when
you exit the container shell.


#### Running the tests

To run the tests, outside of the container, execute:

```
python test_postgresql_94.py
python test_postgresql_95.py
python test_postgresql_96.py
python test_postgresql_10.py
python test_postgresql_11.py
python test_postgresql_12.py
```


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
docker image rm spartacus:tests_postgresql
```
