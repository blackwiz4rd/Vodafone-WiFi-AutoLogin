# Vodafone-WiFi-AutoLogin
Automatic Login to Vodafone-WiFi hotspots in Italy, this script is cross platform so it can be used on any os: Linux, Windows and MacOS.

Versione in italiano - (English version below)
------------

Installazione
-----------
Requisito per far funzionare lo script: requests.
Consiglio l'instalazione tramite pip (https://pip.pypa.io/en/stable/installing/): `pip install requests`.

Prima dell'utilizzo modificare il file `input.txt` inserendo i propri dati (assicurasci che `input.txt` e `vodafone-wifi.py` siano nella stessa cartella)

 Se utilizzate un extender (consiglio NETGEAR PR200, TREK) per connettervi alla rete pubblica Vodafone-WiFi aggiungetelo nella prima riga del file come mostrato negli esempi, altrimenti cancellate la riga o lasciatela come di default

1. `input.txt` Esempio n.1 (SENZA EXTENDER, se ti stai connettendo a Vodafone-WiFi direttamente):
```
username
password
```
2. `input.txt` Esempio n.2 (SE USATE UN EXTENDER):
```
SSID_EXTENDER
username
password
```
Uso
-----
``` 
python vodafone-wifi.py
```

Contributi (Network-Listener)
------------

English version
------------

Installation
-----------
Requirement for the script to work: requests library.        
I suggest installing the library with pip (https://pip.pypa.io/en/stable/installing/): `pip install requests`.

Please, before using edit `input.txt`

 custom_ssid should be used only if you are connecting to a Vodafone-WiFi extender, ohterwise leave empty/default (be sure that `input.txt` and `vodafone-wifi.py` are on the same folder)

1. `input.txt` Example n.1 (NO EXTENDER, if you are connecting to Vodafone-WiFi directly):
```
mario
rossi
```
2. `input.txt` Example n.2 (WITH EXTENDER):
```
NETGEAR
mario
rossi
```
Usage
-----
``` 
python vodafone-wifi.py
```

Contributing (Network-Listener)
------------

See [Contributing](CONTRIBUTING.md)

