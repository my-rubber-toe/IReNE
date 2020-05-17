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

## Deployment System Specifications and dependencies

1. Operating System: CentOS Linux 8 (Core)
2. Architecture:        x86_64
3. CPU(s):              4
4. RAM:                 8GB
5. Python:              3.8.0
5. Node:                v12.6.0
6. Docker:              19.03.8      
7. Docker Compose:      1.25.5

## Firewall Setup

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

After docker is installed, ensure that the docker interface bridge, **docker0**, is part of the `trusted` zone of the firewall. Otherwise, when building the containers, the system will deny traffic via de `docker0` interface and containers will not be built. To verify run the following:

```sh 
  sudo firewall-cmd --zone=trusted --list-interfaces
```

***Note: If the docker0 interface is not part of the listed interfaces add it with the following command***

```sh
  sudo firewall-cmd --permanent --zone=trusted --add-interface=docker0
```

Then reload the firewall with `sudo firewall-cmd --reload`.

## SSL Certificates

For the system to run securely, one must provide a pair of files: certificate file and key file. Create a folder named **ssl-certs** and follow the instructions in the tutorial (HERE)[https://www.humankode.com/ssl/create-a-selfsigned-certificate-for-nginx-in-5-minutes] to create a self signed cerificates.

On a production scale event, please use a certificate file provided by a valid certificate authority.

## Running Compose

Clone all the repositories under the same directory and ensure that all contianers have their respective Dockerfile placed in their directories. Follow the instruccions on each of the directories configuring the Dockerfiles.

Make sure you have the **docker-compose.yml** and **nginx.conf** file in the main directory.

When you run `docker-compose up` on the docker-compose.yml file, a network is created for the containers created and it is added as an interface bridge to the deployment system. To identify this new interface, run `ifconfig` and spot the interface that starts with `br-XXXXXXX`.

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

***For more info on troubleshooting firewall please refer to: https://unix.stackexchange.com/questions/199966/how-to-configure-centos-7-firewalld-to-allow-docker-containers-free-access-to-th***

## Scaling up services

In the event that you wish to scale up the number of services, `docker-compose` allows the scaling of services to any concievable number. To do this, run the following:

```sh
docker-compose up -d --scale <my-service-1>=<nbr> --scale <my-service-2>=<nbr>

Example: docker-compose up -d --scale tellspace-server=5
```

Nginx will automatically load balance the requests to the available services using a Round Robin algorithm.
