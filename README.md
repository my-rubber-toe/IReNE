# IReNE
IReNE is an extension and continuation of the IReN web application.

## Setup

Ensure that the docker bridge, **docker0**, is part of the `trusted` zone of the firewall. To verify run:

```sh 
  sudo firewall-cmd --zone=trusted --list-interfaces
```

***Note: If the docker0 interface is not part of the listed interfaces add it with the follwing command***

```sh
  sudo firewall-cmd --permanent --zone=trusted --add-interface=docker0
```

Then reload the firewall with `sudo firewall-cmd --reload`.

## Running Compose

Ensure that all contianers have their respective Dockerfile placed in their directories. Run `docker-compose up -d` to start all containers.

When you run `docker-compose` on a docker-compose.yml file, a network is created for the containers created and it is added as an interface bridge to the deployment system. To identify this new interface, run `ifconfig` and spot the interface that starts with `br-XXXXXXX`.

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

