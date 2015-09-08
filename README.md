Athena
=============

Athena is a small IRC bot generally designed to be utilitarian features. It's main purpose is to interpret various
esoteric languages (current implementation includes brainf**k, unefunge, and underload). However it supports additional
features such as expression evaluator; character counter; time display; decimal, binary, hexadecimal interconverter.

It only requires the 'pytz' library, which can be feteched (on Ubuntu/Debian) using:

```
apt-get install python-tz
```

Simply run the script using:

./execute.sh "<your IRC user name>" "<initial channel to join>" "<bot nick>"

Messaging 'ath.help' will list all the possible commands that can be passed to Athena.

Athena is licensed as PUBLIC DOMAIN. This means you can wish to do whatever you want with the source, but
at your own risk! (The author is not responsible for any damages caused.)
