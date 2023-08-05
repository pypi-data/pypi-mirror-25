diax
----

This is a python module for interacting with 3DIAX, Authentise's 3D printing API. It's public - we mostly just use it to test stuff.

CHANGELOG
---------

1.18
----
Fix mixing of async/await and yield

1.17
----
Fix a bug with finding users by email address where we always returned None

1.16
----
Add delete function to the commandline diax tool

1.15
----

Add support for custom root certificate authority bundle file to aioclient. Also add internal token authentication support to aioclient

1.14
----
Allow for custom headers in rawput, custom certificate authority bundle file

1.13
----
Add 'rawdelete' to the client for deleting resources

1.12
----
Fix bug with decoding event data stream

1.11
----
Add client.rawput so we can put to a full-formed URL/URI

1.10
----
Add response text to RequestError printout

1.9
---
Add users module and the ability to easily get a user by email address

1.8
---
Fix check for netloc

1.7
---
Don't require more credentials when we have an internal token

1.6
---
Fail gracefully when we can't validate parameters

1.5
---
Add support for token authentication, disabling SSL verification, and the ability to list resources from the CLI

1.4
---
Add support for synchronous generation of events to diax client via client.streamevents()

1.3
---
Add asyncio-based client. It's experimental for now and not very complete

1.2
---
Add basic CLI with client-side validation for doing general operations with diax

1.1
---
Allow login, pull credentials from a well-known file

1.0
---
Initial release, does, literally, nothing.
