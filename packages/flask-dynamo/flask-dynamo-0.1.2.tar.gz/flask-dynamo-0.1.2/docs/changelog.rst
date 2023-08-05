.. _changelog:


Change Log
==========

All library changes, in descending order.


Version 0.1.2
-------------

**Released on September 6, 2017.**

- Fixing init issues.


Version 0.1.1
-------------

**Released on August 21, 2017.**

- Added support for shared boto3 session.


Version 0.1.0
-------------

**Released on August 21, 2017.**

- Added support for flask app factory and traditional methods of initialization.
- Added documentation for boto3.
- Fixed reuse of DynamoDB connections across requests.
- Optimized tests to run faster.
- Added support for ``AWS_SESSION_TOKEN``.  Thanks `@vbisserie
  <https://github.com/vbisserie>`_ for the code!


Version 0.0.8
-------------

**Released on August 1, 2017.**

- Improving the ``create_all`` management command so it won't error out when
  attempting to re-create already created tables.  Thanks `@amir-beheshty
  <https://github.com/amir-beheshty>`_ for the codez!


Version 0.0.7
-------------

**Released on May 25, 2015.**

- Fixing deferred initialization of app object.  Thanks `@jpanganiban
  <https://github.com/jpanganiban>`_ for the fix!


Version 0.0.6
-------------

**Released on March 29, 2015.**

- Allowing users to specify ``DYNAMO_TABLES`` dynamically =)  This makes it
  possible to specify your tables dynamically instead of immediately at startup.


Version 0.0.5
-------------

**Released on March 29, 2015.**

- Merging PR for improved environment variable detection using boto.  We'll now
  allow the user to configure Flask-Dynamo through all of the standard boto
  methods.


Version 0.0.4
-------------

**Released on November 17, 2014.**

- Adding support for DynamoDB Local!


Version 0.0.3
-------------

**Released on November 17, 2014.**

- Fixing packaging issues with import ordering.  Thanks @alastair for the
  report!


Version 0.0.2
-------------

**Released on June 21, 2014.**

- Adding tests.
- Adding docs.
- Adding logo.
- Slight refactoring.


Version 0.0.1
-------------

**Released on June 21, 2014.**

- First release!
- Basic functionality.
