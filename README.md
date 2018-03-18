# Vodafone-WiFi-AutoLogin
Automatic Login to Vodafone-WiFi hotspots in Italy, this script is cross platform so it can be used on any os: Linux, Windows and MacOS.<br />
Thanks to Mirco (https://github.com/Emmegiemme) who helped me making a better script for you.<br />

Versione in italiano - (English version below)
------------

Installazione
-----------
Clonate questa repository `git clone https://github.com/blackwiz4rd/Vodafone-WiFi-AutoLogin ~/Downloads/`<br />
Requisiti per eseguire lo script python si trovano in `install_pip_requirements.sh`.<br />
È richiesta l'installazione di python e pip.<br />
Per scaricare python: `https://www.python.org/downloads/`.<br />
Per scaricare pip su MacOS: `curl -o ~/Downloads/get-pip.py https://bootstrap.pypa.io/get-pip.py`.<br />
Per scaricare pip su Linux: `wget https://bootstrap.pypa.io/get-pip.py ~/Downloads/get-pip.py`.<br />
Per scaricare pip su Windows accedete tramite browser a `https://bootstrap.pypa.io/get-pip.py` e salvate il file nella cartella Downloads.<br />
Per installare pip:  `cd ~/Downloads/get-pip.py` ed eseguite `python get-pip.py`.<br />
Dopo aver installato python e pip eseguite `./install_pip_requirements.sh`<br />

Configurazione per utenti
-----------
Assicurasci che `vodafone.config` e `vodafone.py` siano nella stessa cartella.<br />
Modificate i campi inserendo i vostri dati.<br />
Esempi di configurazione:<br />
È necessario essere connessi a Vodafone-WiFi affinchè il programma abbia effetto altrimenti verrà interrotta la sua esecuzione.<br />
Usate `loop=True` solo se volete verificare se siete connessi alla rete ogni minuto da quando il programma è avviato. Se ci sono state disconnessioni inaspettate il programma tenterà di riconnettersi automaticamente con i vostri dati.<br />
Usate `force=True` solo se ottenete NotConnectedToVodafoneWiFiException durante l'esecuzione e siete connessi ad una rete Vodafone-WiFi<br />
1. `vodafone.config` Esempio n.1 (Utente Vodafone Italia):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_IT
loop=False
force=False
```
2. `vodafone.config` Esempio n.2 (Utente Vodafone Spagna):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_ES
loop=False
force=False
```
3. `vodafone.config` Esempio n.3 (Utente Pass Customer):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=
loop=False
force=False
```
4. `vodafone.config` Esempio n.4 (Utente Fon Roaming Partner):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=FON_ROAM
loop=False
force=False
```
Uso per utenti
-----
```
cd ~/Downloads/Vodafone-WiFi-AutoLogin/
python vodafone.py
```

------------

English version - (Italian version above)
------------

Installation requirements
-----------
Clone this repository `git clone https://github.com/blackwiz4rd/Vodafone-WiFi-AutoLogin ~/Downloads/`<br />
Requirements to install the scrip are available in `install_pip_requirements.sh`.<br />
It is required to install python and pip.<br />
To download python: `https://www.python.org/downloads/`.<br />
To download pip on MacOS: `curl -o ~/Downloads/get-pip.py https://bootstrap.pypa.io/get-pip.py`.<br />
To download pip on Linux: `wget https://bootstrap.pypa.io/get-pip.py ~/Downloads/get-pip.py`.<br />
To download pip on Windows use a web broswer `https://bootstrap.pypa.io/get-pip.py` and save this file in the Downloads folder.<br />
To install pip:  `cd ~/Downloads/get-pip.py` and execute `python get-pip.py`.<br />
After installing pip make sure the requirements are satisfied, run `./install_pip_requirements.sh`<br />


How to setup for users
-----------
Be sure `vodafone.config` and `vodafone.py` are in the same folder.<br />
Change the fields according to your configuration.<br />
Configuration examples:<br />
It is required to be connected to a Vodafone-WiFi in order to login to the hotspot, otherwise the execution will be interrupted.<br />
Use `loop=True` only if you want to check if you are connected to the network each minute from when the program was started. If there were any disconnections the script will automatically try to connect with your configuration.<br />
Use `force=True` only if you are getting a NotConnectedToVodafoneWiFiException and you are sure to be connected to a Vodafone-WiFi network.<br />
Configuration examples:<br />
1. `vodafone.config` Example n.1 (Vodafone Italia user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_IT
loop=False
force=False
```
2. `vodafone.config` Example n.2 (Vodafone Spain user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_ES
loop=False
force=False
```
3. `vodafone.config` Example n.3 (Pass Customer user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=
loop=False
force=False
```
4. `vodafone.config` Example n.4 (Fon Roaming Partner user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=FON_ROAM
loop=False
force=False
```
How to run the script for users
-----
```
cd ~/Downloads/Vodafone-WiFi-AutoLogin/
python vodafone.py
```
------------

An additional curl script was added if you wish to use curl only to login
-----
```
./curl_script.sh
```
------------
