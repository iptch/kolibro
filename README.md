# Kolibro 

A morango client for load testing

## Setup 

Currently there is no setup.py  
Make sure to use the same environment as the morango project.

There are no additional requirements added at this point.

To get started with django the following resources were uses:  
- https://docs.djangoproject.com/en/4.2/intro/tutorial01/

## Get Started - Or Django in 5 Minutes

1. `manage.py` is your python entrypoint. 
2. Run django commands with ``python manage.py --help``
3. Run your initial migration to be in sync wiht everything that comes with django ``python manage.py migrate``
4. To start your server simple run ``python manage.py runserver`` and you will start your devserver under ``localhost:8000``

If you want to add models to django you have to create a migration: ``python mananage.py makemigration``

Run tests with ``python manage.py test client`` 

python manage.py migrate --run-syncdb 

## Integrate Morango

### Syncable Model

### Hooks

### Session

MorangoProfileController controlls your network communication

### Store  

### Buffer

### Calculate Diff

### Authentication 

Morango uses certificates to verify the authenticity of exchanging clients

A client opens a connection with two certificates. A client certificate and a remote certificate.
The client certificate has to signed by the remote certificate.

#### Signing Client

A client can request a signed certificate by another client that is already in the chain of trust. 
The request contains:
- The desired remote certificate that should be used to sign.
  The remote client has to have the private key of the signing certificate.
- The scope id that should be applied. 
- The scope parameters to apply to the scope
- The user arguments in order to authenticate against the other client
  This is necessary because up to this point you are not identifiable by the other client
- Password for the user.
  Currently morango only supports basic auth for this initial certificate signing

#### Distributing Trust

A client can request all owned certificates by another client.
A client can also push signed certificates in order to distribute signed certificates to other peers. This requires a flag ALLOW_CERTIFICATE_PUSHING to be set.

A client has to have your signed certificate and the singing certifacate before it can trust you.

#### User Model

To establish an initial trust Morange requires a basic authentication with username and password. This mechanism is hooked into django framework. 
To manage permissions regarding certificate singing a user has to implement a `has_morango_certificates_scope_permission` method.

### Authorization

#### ScopeDefinitions




Cert exchange

- SyncableModelRegistry




