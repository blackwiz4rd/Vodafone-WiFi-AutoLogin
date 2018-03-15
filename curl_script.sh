#!/bin/sh

URL=$(curl -Ls -w %{url_effective} http://google.com)
URL=${URL:0:47}login${URL:53:165}
echo "$URL"
DATA=chooseCountry=VF_IT%2F&userFake=your-email@provider.com&UserName=VF_IT%2Fyour-email@provider.com&Password=your-password&rememberMe=true&_rememberMe=on
curl --data "${DATA}" ${URL}
