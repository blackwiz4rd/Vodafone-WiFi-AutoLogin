# Vodafone-WiFi-AutoLogin
Automatic Login to Vodafone-WiFi hotspots in Italy

Versione in italiano - (English version below)
------------

Installazione
-----------
Prima dell'utilizzo modificare il file `input.txt` inserendo i propri dati

 Se utilizzate un extender (consiglio NETGEAR PR200, TREK) per connettervi alla rete pubblica Vodafone-WiFi aggiungetelo nella prima riga del file come mostrato negli esempi, altrimenti lasciate la riga VUOTA

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
Please, before using modify `input.txt`

 custom_ssid should be used only if you are connecting to a Vodafone-WiFi extender, ohterwise leave BLANK

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

