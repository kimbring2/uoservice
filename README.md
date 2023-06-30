# UoService - Ultima Online Learning environment
UoService is a service to play Ultima Online through gRPC. There are first-class Python bindings and examples, so you can play Ultima Online as you would use the OpenAI gym API.

# Quick Start Guide
## Get UoService

The easiest way to get UoService is to use pip:
$ git clone https://github.com/kimbring2/uoservice
$ cd uoservice
$ pip install .

That will install the uoservice package along with all the required dependencies. virtualenv can help manage your dependencies. You may also need to upgrade pip: pip install --upgrade pip for the uoservice install to work.

# Get Ultima Online
Because Ultime Online is an MMORPG game, there is basically a central server. To run UoService, a server must be installed as well. Please visit the [ServUO site](https://github.com/ServUO/ServUO) and set up the server.

Next, you need to download a modified client in which gRPC part for communication with Python is added to the original ClassicUO from [Google Drive](https://drive.google.com/file/d/1-7EqQp59LtJUk3hZVraHtawe6MPK-SPi/view?usp=sharing).

