# UoService
<img src="images/UoServiceMain.png" width="400">

UoService is a service to play Ultima Online through gRPC. There are first-class Python bindings and examples, so you can play Ultima Online as you would use the OpenAI gym API.

# Architecture
<img src="images/CodeArchitecture.png" width="600">

# System requirement
Currently, I test this project in Ubuntu linux only.

# Quick Start Guide
## Get UoService

The easiest way to get UoService is to use pip:

```
$ git clone https://github.com/kimbring2/uoservice
$ cd uoservice
$ pip install .
```

That will install the UoService package along with all the required dependencies. Virtualenv can help manage your dependencies. You may also need to upgrade pip: ```pip install --upgrade pip``` for the UoService installs to work.

# Get Server and gRPC client of Ultima Online
Because Ultime Online is an MMORPG game, there is basically a central server. To run UoService, a server must be installed as well. Please visit the [ServUO site](https://github.com/ServUO/ServUO) and set up the server.

Next, you need to build a modified ClassicUO client form [PyUO](https://github.com/kimbring2/pyuo).

Because UoService does not have the function to create an account on its own, you must create an account using the original ClassicUO before using the modified client.

Finally, some values ​​inside ```settings.json``` must be changed according to the location where ServeUO and Ultima Online game are installed with Ubuntu [Wine](https://wiki.winehq.org/Ubuntu).

<img src="images/server_settings.png" width="800">

# Run an agent 
Make sure to run the ServeUO before running the client.
```
$ mono ServUO.exe
```

Unlike the original client, the client for UoService must operate most of the operations through argument setting.

Run the [sample Python Application](https://github.com/kimbring2/uoservice/blob/main/uoservice/examples/semaphore_sync.py).
```
$ python examples/semaphore_sync.py --grpc_port 60051
```

## 3.No gRPC communication with Python, Replay saving
```
$ ./ClassicUO -username [Account ID] -password [Account PWD] -window_width [Screen Width] -window_height [Screen Height] -replay
e.g. ./ClassicUO -username kimbring2 -password kimbring2 -human_play -window_width 1370 -window_height 1280 -replay
```
