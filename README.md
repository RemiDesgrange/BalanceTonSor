Test

# Balance Ton SOR

This little program help you translate SOR files (from reflectormeter) to json. To process a SOR simplfy send it via post (curl -X POST --data-binary @file.sor http://localhost/)

PR are welcome. This app may return non expected result.

This work has been made possible by the excellent work of [https://github.com/sid5432/pyOTDR](https://github.com/sid5432/pyOTDR)

## Install

**⚠  This app is python2 !! ⚠**

Any compliant wsgi server is capable of running this little app. No database. No storage. Just this
stateless app. Yes it's webscale.


Quick and dirty:

```
# use any method to create an env.
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
gunicorn main.app
```

## Contribute

I'll gladly accept PR. But maybe create an issue first 😏.

## It doesn't work well with my SOR file

Contribute then !! I you don't know how to do it. Drop me a mail.

## About the name

Don't care too much about the name please.

