Flask-WebSub
-------------

An implementation of a WebSub hub, publisher and subscriber as a Flask
extension. The implementation is meant to be used as a library that can be
integrated in a larger application.

The components are split up into multiple packages, so you don't necessarily
have to use all three. It is for example possible to use the subscriber
implementation with an external hub. To learn to use this package, take a look
at the client_example.py (subscriber) and server_example.py (hub/publisher)
files. Next to that, the public classes and functions of the package all have
doc strings which can be inspected using the built-in python ``help()``
function.

If you do use both the publisher and hub package in the same app, you benefit
from autodiscovery of the hub url.

Using the flask_websub.hub package requires celery.

For more about WebSub, see its specification: https://www.w3.org/TR/websub/


Examples
--------

To run the examples, first setup a celery broker. I myself did it this way:

```
docker run -p 6379:6379 redis:alpine
```

Then, it's time to update server_example.py and client_example.py's SERVER_NAME
config variable. Simply set them to whatever hostname the server will have (it
can just be localhost).

I recommend installing the dependencies in a virtualenv:

```
python3 -m venv venv # create the virtualenv
source venv/bin/activate # activate the virtualenv
pip install -e .[celery,redis] # install the dependencies
```

Finally, it's time to start the applications. Each line in a different
terminal (assuming the virtualenv is active in each):

```
celery -A server_example.celery worker -l info
./server_example.py
./client_example.py
```
