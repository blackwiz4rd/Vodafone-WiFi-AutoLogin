# Vodafone-WiFi-AutoLogin
Automatic Login to Vodafone-WiFi hotspots in Italy, this script is cross platform so it can be used on any os: Linux, Windows and MacOS.
Thanks to Mirco (gallo.mirco@gmail.com) who helped me making a better script for you.

Versione in italiano - (English version below)
------------

Installazione per sviluppatori
-----------
Requisito per eseguire lo script python: requests, configparser.
Consiglio l'instalazione tramite pip (https://pip.pypa.io/en/stable/installing/): `pip install requests`.
Consiglio l'instalazione tramite pip: `pip install configparser`.

Configurazione per utenti (Non è necessario utilizzare python, c'è già una versione precompilata)
-----------
Per utilizzare la versione compilata, nella directory `dist` modificare il file `vodafone.config` inserendo i propri dati (assicurasci che `vodafone.config` e `vodafone` siano nella stessa cartella)

Esempi di configurazione:
È necessario essere connessi a Vodafone-WiFi affinchè il programma abbia effetto altrimenti verrà interrotta la sua esecuzione.
Usate `loop=True` solo se volete verificare se siete connessi alla rete ogni minuto da quando il programma è avviato. Se ci sono state disconnessioni inaspettate il programma tenterà di riconnettersi automaticamente con i vostri dati.
1. `vodafone.config` Esempio n.1 (Utente Vodafone Italia):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_IT
loop=False
```
2. `vodafone.config` Esempio n.2 (Utente Vodafone Spagna):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_ES
loop=False
```
3. `vodafone.config` Esempio n.3 (Utente Pass Customer):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=
loop=False
```
4. `vodafone.config` Esempio n.4 (Utente Fon Roaming Partner):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=FON_ROAM
loop=False
```
Uso per utenti
-----
```
cd dist
```
```
./vodafone
```
oppure
```
vodafone
```
da qualsiasi shell del terminale dopo aver copiato la versione compilata in /usr/bin/ tramite
`sudo cp dist/* /usr/bin/`
`sudo chmod +x /usr/bin/vodafone`

------------

English version - (Italian version above)
------------

Installation requirements for developers
-----------
Requirements to run the script: requests, configparser.
I suggest installing using pip (https://pip.pypa.io/en/stable/installing/): `pip install requests`.
I suggest installing pip: `pip install configparser`.

How to setup for users
-----------
To use the compiled version, modify `vodafone.config` inside  `/dist` diectory by adding your settings (be sure `vodafone.config` and `vodafone` are in the same folder)

Configuration examples:
It is required to be connected to a Vodafone-WiFi in order to login to the hotspot, otherwise the execution will be interrupted.
Use `loop=True` only if you want to check if you are connected to the network each minute from when the program was started. If there were any disconnections the script will automatically try to connect with your configuration.

Configuration examples:
1. `vodafone.config` Example n.1 (Vodafone Italia user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_IT
loop=False
```
2. `vodafone.config` Example n.2 (Vodafone Spain user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=VF_ES
loop=False
```
3. `vodafone.config` Example n.3 (Pass Customer user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=
loop=False
```
4. `vodafone.config` Example n.4 (Fon Roaming Partner user):
```
[config]
username=your-account@your-provider.com
password=your-password
customer=FON_ROAM
loop=False
```
How to run the script for users
-----
```
cd dist
```
```
./vodafone
```
or I suggest copying the compiled version in /usr/bin/ via
`sudo cp dist/* /usr/bin/`
`sudo chmod +x /usr/bin/vodafone`
and executing from any shell
```
vodafone
```
------------
