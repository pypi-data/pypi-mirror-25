# klue-microservice

Easily create and deploy a Flask-based REST api running as a Docker container
on amazon AWS Elastic Beanstalk.

[klue-microservice](https://github.com/erwan-lemonnier/klue-microservice) uses
[klue-client-server](https://github.com/erwan-lemonnier/klue-client-server) to
spawn REST apis into a Flask app. These apis are defined as swagger
specifications, describing all API endpoints in a friendly yaml format, and
binding endpoints to Python methods.

[klue-microservice](https://github.com/erwan-lemonnier/klue-microservice) uses
[klue-microservice-deploy](https://github.com/erwan-lemonnier/klue-microservice-deploy)
to easily deploy the micro service as a Docker container running inside Amazon
Elastic Beanstalk.

With [klue-microservice](https://github.com/erwan-lemonnier/klue-microservice),
you get out-of-the-box:

* A best practice auto-scalling setup on Elastic Beanstalk
* Error handling and reporting around your api endpoints
* Endpoint authentication based on JWT tokens
* Python objects for all your api's json data, with silent
marshalling/unmarshalling and validation

Easy peasy now you happy!

## Example

See
[klue-microservice-helloworld](https://github.com/erwan-lemonnier/klue-microservice-helloworld)
for an example of a minimal REST api implemented with klue-microservice, and
ready to deploy on docker containers in Amazon EC2.

## Installation

```
pip install klue-microservice
pip install klue-microservice-deploy
```

## Synopsis

A REST api microservice built with klue-microservice has a directory tree
looking like this:

```
.
├── apis                       # Here you put the swagger specifications both of the apis your
│   └── myservice.yaml         # server is implementing, and of eventual other apis your server
│   └── login.yaml             # is in its turn caling
│   └── profile.yaml           # See klue-client-server for the supported yaml formats.
|
├── myservice                  # Here is the code implementing your server api's endpoints
│   └── api.py
│
├── LICENSE                    # You should always have a licence :-)
├── README.rst                 # and a readme!
|
├── klue-config.yaml           # Config for klue-microservice and klue-microservice-deploy
|
├── server.py                  # Code to start your server, see below
|
└── test                       # Standard unitests, executed with nosetests
|   └── test_pep8.py
|
└── testaccept                 # Acceptance tests against api endpoints
    ├── test_v1_user_login.py  # Best practice: name test files after the endpoint they test
    └── test_version.py        # -> Here to test the generic /ping, /version and /auth/version endpoints

```

And your server simply looks like:

```python
import os
import sys
import logging
from flask import Flask
from klue_microservice import API, letsgo


log = logging.getLogger(__name__)

# WARNING: you must declare the Flask app as shown below, keeping the variable
# name 'app' and the file name 'server.py', since gunicorn is configured to
# lookup the variable app inside the code generated from server.py.

app = Flask(__name__)
# Here you could add custom routes, etc.


def start(port=80, debug=False):

    # Your swagger api files are under ./apis, but you could have them anywhere
    # else really.

    here = os.path.dirname(os.path.realpath(__file__))
    path_apis = os.path.join(here, "apis")

    # Tell klue-microservice to spawn apis inside this Flask app.  Set the
    # server's listening port, whether Flask debug mode is on or not, and, if
    # some of your endpoints use klue-microservice's builtin JWT token-based
    # authentication scheme, initialise a jwt token and audience

    api = API(
        app,
        port=port,
        debug=debug,
        jwt_secret=os.environ.get("KLUE_JWT_SECRET"),
        jwt_audience=os.environ.get("KLUE_JWT_AUDIENCE"),
        jwt_issuer=os.environ.get("KLUE_JWT_ISSUER"),
    )

    # Find all swagger files and load them into klue-client-server

    api.load_apis(path_apis)

    # Optinally, publish the apis' specifications under the /doc/<api-name>
    # endpoints
    # api.publish_apis()

    # Start the Flask app and serve all endpoints defined in
    # apis/myservice.yaml

    api.start(serve="myservice")


# Let klue-microservice handle argument parsing...
letsgo(__name__, callback=start)
```

You start your server in a terminal like this:

```bash
cd projectroot
python server.py --port 8080
```

You run acceptance tests against the above server like this:

```bash
cd projectroot
run_acceptance_tests --local
```

## Deep dive

### Installing

```
pip install klue-microservice
```

### Swagger specifications

All api endpoints that your service needs, both those it implements and those
it calls as a client, are to be defined as swagger specifications in the format
supported by
[klue-client-server](https://github.com/erwan-lemonnier/klue-client-server).
klue-client-server uses [Bravado](https://github.com/Yelp/bravado) to handle
marshalling/unmarshalling and validation of your api objects to and from json,
and does all the magic of spawning client and server stubs for all api
endpoints, as well as supporting optional database serialization for your api
objects.

### JWT authentication

klue-microservice allows you to add JWT token authentication around the
endpoints that require authentication.

Authentication is achieved by passing a JWT session token in the HTTP
Authorization header:

```Authorization: Bearer {session token}```

Your service may generate JWT tokens using the 'generate_token()' method from
[klue-microservice.auth](https://github.com/erwan-lemonnier/klue-microservice/blob/master/klue_microservice/auth.py).

The JWT issuer, audience and secret are passed when starting the service, as
arguments to the 'API()' constructor. By default, tokens are valid for 24
hours.

### Error handling and reporting

If an endpoint raises an exception, it will be caught by klue-microservice and returned
to the caller in the form of an Error json object looking like:

```
{
    "error": "INVALID_USER",                      # Code identifying this error
    "error_description": "DB entry not found",    # Developer friendly explanation
    "user_message": "Sorry, we don't know you",   # User friendly explanation (optional)
    "status": 401                                 # Same as the response's HTTP status code
}
```

You can create your own errors by subclassing the class
[KlueMicroServiceException](https://github.com/erwan-lemonnier/klue-microservice/blob/master/klue_microservice/exceptions.py)
and return them at any time as json reply as follows:

```
from klue_microservice.exceptions import KlueMicroServiceException

class InvalidUserError(KlueMicroServiceException):
    code = 'INVALID_USER'        # Sets the value of the 'error' field in the error json object
    status = 401                 # The HTTP reply status, and 'status' field of the error json object

# An endpoint implementation...
def do_login(userdata):
    return MyException("Sorry, we don't know you").http_reply()
```

When an exception occurs in your endpoint, you have the choice of:

* If it is a fatal exception, return a KlueMicroServiceException to the caller as shown above.

* If it is a non-fatal error, you can just ignore it, or you can send back a
crash report to the service's admins. This is done by providing the 'API'
constructor with an 'error_reporter' callback:

```
from klue_microservice import API, letsgo

def my_crash_reporter(title, message):
    # title is a short description of the error, while message is a full crash
    # dump, containing a traceback of the exception caught, data on the caller
    # and runtime, etc. Now, send it to who you want!
    send_email(to='admin@mysite.com', subject=title, body=message)
    tell_slack(channel='crashes', msg="%s\n%s" % (title, message))

api = API(
    app,
    port=port,
    debug=debug,
    error_reporter=my_crash_reporter,
    ..
)
```

### Testing strategy

klue microservices are developed around two sets of tests:

* Standard Python unitests that should be located under 'test/' and will be
executed via nosetests at the start of the deployment pipeline.

* Blackbox acceptance tests that target the apis endpoints, and are executed
via the tool
[run_acceptance_tests](https://github.com/erwan-lemonnier/klue-microservice/blob/master/bin/run_acceptance_tests)
that comes packaged with klue-microservice. Those acceptance tests should be
located under the 'testaccept' dir, and it is recommended to name them after
the endpoint they target. So one test file per tested API endpoint. Acceptance
tests are designed to be executed against a running instance of the API server,
be it a server you are running locally in a separate terminal, a docker
container, or a live instance in Elastic Beanstalk.  Those tests should
therefore treat the API as a blackbox and focus solely on making API calls and
testing the results. API calls should be made using test methods from
[klue-unit](https://github.com/erwan-lemonnier/klue-unit). See
[klue-microservice-helloworld](https://github.com/erwan-lemonnier/klue-microservice-helloworld/blob/master/testaccept/test_version.py)
for an example of acceptance test.

### Deployment pipeline

Klue microservices come with a ready-to-use deployment pipeline that packages
the service as a docker image and deploys it on Amazon Elastic Beanstalk with
minimal configuration.

For details, see
[klue-microservice-deploy](https://github.com/erwan-lemonnier/klue-microservice-deploy).

### Elastic Beanstalk configuration

The Klue microservice toolchain is built to deploy services as Docker images
running inside Amazon EC2 instances in Elastic Beanstalk, behind an Elastic
Load Balancer. All the details of setting up those Amazon services is handled
by [klue-microservice-deploy] and should be left untouched. A few parameters can be
adjusted, though. They are described in the 'klue-config.yaml' section below.

### klue-config.yaml

The file 'klue-config.yaml' is the one place to find all configurable aspects
of a 'klue-microservice'. The file accepts the following attributes:

* 'name' (MANDATORY): a short name for this project, used when naming elastic
beanstalk environments.

* 'live_host' (MANDATORY): url to the live server running this api.

* 'env_jwt_secret', 'env_jwt_audience', 'env_jwt_issuer' (OPTIONAL): name of
  environment variables containing respectively the JWT secret, JWT audience
  and JWT issuer used for generating and validating JWT tokens. Not needed if
  the API does not use authentication.

* 'env_secrets' (OPTIONAL): names of environemt variables that will be passed
  to Elastic Beanstalk and loaded into Docker containers at runtime in Elastic
  Beanstalk . This is the recommended way of passing secrets to the container
  without commiting them inside your code.

The following variables are needed if you want to deploy to Elastic Beanstalk
using klue-microservice-deploy:

* 'aws_user' (MANDATORY): name of the IAM user to use when creating the
  Beanstalk environment (see
  [klue-microservice-deploy](https://github.com/erwan-lemonnier/klue-microservice-deploy)
  for details).

* 'aws_keypair' (MANDATORY): name of the ssh keypair to deploy on the server's
  EC2 instances.

* 'aws_instance_type' (MANDATORY): the type of EC2 instance to run servers on
  (ex: 't2.micro').

* 'aws_cert_arn' (OPTIONAL): amazon ARN of a SSL certificate to use in the
  service's load balancer. If specified, the live service will be configured to
  listen on port 443 (https). If not, if will listen on port 80 (http).

* 'docker_repo' (MANDATORY): name of the hub.docker.com organization or user to
  which to upload docker images (see
  [klue-microservice-deploy](https://github.com/erwan-lemonnier/klue-microservice-deploy)
  for details).

* 'docker_bucket' (MANDATORY): name of the Amazon S3 bucket to which to upload
  the service's Amazon configuration (see
  [klue-microservice-deploy](https://github.com/erwan-lemonnier/klue-microservice-deploy)
  for details).

[Here is an
example](https://github.com/erwan-lemonnier/klue-microservice-helloworld/blob/master/klue-config.yaml)
of 'klue-config.yaml'.

### Built-in endpoints

The following endpoints are built-in into every klue-microservice instance, based
on [this swagger spec](https://github.com/erwan-lemonnier/klue-microservice/blob/master/klue_microservice/ping.yaml):

```
# Assuming you did in a separate terminal:
# $ python server.py --port 8080

$ curl http://127.0.0.1:8080/ping
{}

$ curl http://127.0.0.1:8080/version
{
  "container": "",
  "name": "ping",
  "version": "0.0.1"
}

$ curl http://127.0.0.1:8080/auth/version
{
  "error_description": "There is no Authorization header in the HTTP request",
  "error_id": "17f900c8-b456-4a64-8b2b-83c7d36353f6",
  "status": 401,
  "error": "AUTHORIZATION_HEADER_MISSING"
}

$ curl -H "Authorization: Bearer eyJpc3M[...]y8kNg" http://127.0.0.1:8080/auth/version
{
  "container": "",
  "name": "ping",
  "version": "0.0.1"
}

```
