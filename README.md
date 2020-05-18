# IReNE
IReNE is an extension and continuation of the IReN web application. Consists of 8 microservices:

1. Reverse Proxy - service responsible for redirecting traffic to the corresponding services, filtering HTTPS traffic to HTTP, load balancing and more.
2. Database - service that holds the information to be used by the services.
3. SearchSpace UI - service that holds the user interface for visualization of documents present in the database.
4. SearchSpace Server - api service responsible for returning the information to the search space user interface.
5. TellSpace UI - service that holds the user interface for the generation and editing of documents.
6. TellSpace Server - api service that is responsible for updating the edited information on the tellspace user interface and updating records in the database.
7. Admin UI - server that holds the user interface for administrative operations.
8. Admin Server - api service responsible of performint the operations given by the admin user interface. 


The management system for the services is `docker-compose`. Please review the documentation for any trouble regarding container management.
(Docker Compose Documentation)[https://docs.docker.com/compose/]

## Deployment System Specifications and dependencies

1. Operating System: CentOS Linux 8 (Core)
2. Architecture:        x86_64
3. CPU(s):              4
4. RAM:                 8GB
5. Python:              3.8.0
5. Node:                v12.6.0
6. Docker:              19.03.8      
7. Docker Compose:      1.25.5

## Setup: Directory Structure

Download each of the services into a common directory and create two new directories with names `ssl-certs` and `logs`. Also, copy the contents of the files `nginx.conf`, `interface_setup.sh`, `init-mongo.js` and `docker-compose.yml`:

```
/IReNE-Database/
/IReNE-admin-server/
/IReNE-admin-ui/
/IReNE-searchspace-server/
/IReNE-searchspace-ui/
/IReNE-tellspace-server/
/IReNE-tellspace-ui/
/logs/
/ssl-certs/
docker-compose.yml
init-mongo.js
interface_setup.js
nginx.conf
```

Follow the instructions on each of the repositories to setup the services.

## Setup: SSL Certificates

For the system to run securely, one must provide a pair of files: certificate file and key file. Create a folder named **ssl-certs** and follow the instructions in the tutorial (HERE)[https://www.humankode.com/ssl/create-a-selfsigned-certificate-for-nginx-in-5-minutes] to create a self signed cerificates.

On a production scale event, please use a certificate file provided by a valid certificate authority. 

## Setup: Database credentials

Access the `init-mongo.js` file and configure the file by setting the names of the database user, password and database name to use.

## Setup: Docker Compose File

The `docker-compose.yml` file is the main controller of the services. Please follow the instrucctions presented in the file and make sure that all files are mapped correctly.

***Note: The database SHOULD NOT expose port 27017 of the deployment system unless testing is being performed. To avoid exposing the database, simply comment the "ports" section of the "irene-db" service.***

## Setup: System Firewall

CentOS by default, has its firewall blocking all ports. Firewall security is divided into many zones but the ones that we are interested are **public** and **trusted** zones.

First ensure that in the public firewall zone has ports 80 and 443 enabled. To list the port in the public zone write the following command:

```sh 
  sudo firewall-cmd --zone=public --list-ports
  
  Example response:
  
  80/tcp 443/tcp
```

If the system doesn't have the ports added to the zone, write the following commands.:

```sh 
  sudo firewall-cmd --zone=public --permanent --add-port=80/tcp
  sudo firewall-cmd --zone=public --permanent --add-port=443/tcp
  sudo firewall-cmd --reload
```

Ensure that the docker bridge, **docker0**, is part of the `trusted` zone of the firewall. Otherwise, when building the containers, the system will deny traffic via de `docker0` interface and containers will not be built. To verify run the following:

```sh 
  sudo firewall-cmd --zone=trusted --list-interfaces
```

***Note: If the docker0 interface is not part of the listed interfaces add it with the follwing command***

```sh
  sudo firewall-cmd --permanent --zone=trusted --add-interface=docker0
```

Then reload the firewall with `sudo firewall-cmd --reload`.

## Running Compose

Ensure that all contianers have their respective Dockerfile placed in their directories. Run `docker-compose up -d` to start all containers. If the service container has not been built, `docker-compose` will build and then run the containers.

When you run `docker-compose` on a docker-compose.yml file, an internal network is created for the containers and it is added as an interface bridge to the deployment system. To identify this new interface, run `ifconfig` and spot the interface that starts with `br-XXXXXXX`.

Copy the interface name and run the following command to add it to the trusted interfaces of the firewall:

```sh
  sudo firewall-cmd --permanent --zone=trusted --add-interface=<your-br-interface>
```

Example: `sudo firewall-cmd --permanent --zone=trusted --add-interface=br-123456789`

Then reload the firewall with `sudo firewall --reload`.


## Removing unwanted interfaces

Run the follwing to list the interfaces:

```sh 
  sudo firewall-cmd --zone=trusted --list-interfaces
```

Select one of the interfaces and run:

```sh
  sudo firewall-cmd --permanent --zone=trusted --remove-interface=<your-br-interface>
```

Then reload the firewall with `sudo firewall --reload`.

***For more infor on troubleshooting firewall please refer to: https://unix.stackexchange.com/questions/199966/how-to-configure-centos-7-firewalld-to-allow-docker-containers-free-access-to-th***

## Scaling up services

In the event that you wish to scale up the number of services, `docker-compose` allows the scaling of services to any concievable number. To do this, run the following:

```sh
docker-compose up -d --scale <my-service-1>=<nbr> --scale <my-service-2>=<nbr>

Example: docker-compose up -d --scale tellspace-server=5
```

Nginx will automatically load balance the requests to the available services using a Round Robin algorithm.

## Updating Services

If a particular needs to be updated, navigate to said service folder and update it using *git* controls. After changes have been applied, navigate to the main directory of the services. Once you have reach the main directory, run the following to stop and remove the container with the service to be updated:

```sh
docker-compose stop <service-to-be-updated>
docker-compose rm <service-to-be-updated>
```

Once the container has been removed, the service image must be rebuilt using `docker-compose build <service-to-be-updated>`. Finally, when the image has been rebuilt, simply create a new container instance as such:

```sh
docker-compose up -d <service-to-be-updated> 
```

The service should be updated.

