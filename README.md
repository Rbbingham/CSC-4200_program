## Project for CSC 4200
Implementation of a client and a sever program that will send a command over a network
 
### Server specifications
The server takes two arguments:

```lightserver -p <PORT> -l <LOG FILE LOCATION>```

1. ```PORT``` - The port the server listens on.
2. ```LOG FILE LOCATION``` - Where you will keep a record of actions

### Client specifications
The client takes three arguments:

```lightclient -s <SERVER-IP> -p <PORT> -l <LOG FILE LOCATION>```

1. ```SERVER-IP``` - The IP address of the server
2. ```PORT``` - The port the server listens on.
3. ```LOG FILE LOCATION``` - Where you will keep a record of actions