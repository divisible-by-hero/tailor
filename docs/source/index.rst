.. Tailor documentation master file, created by
   sphinx-quickstart on Mon Mar  5 15:24:28 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Tailor
=================

Tailor is a Python (Django) application designed to take your fabric commands, and make them executable from an API.  Tailor is built with modularity in mind by binding explicitly to the Fabric file you supply.  Fabric commands can be made accessible to the web API by adding the @tailored decorator.


.. toctree::
   :maxdepth: 2
   
   quick_start
   authors
   decorators
   api/server
   license



Feature Set
-----------

* Drop in fabfile
* Execute decorated functions through a HTTP based API.
* Key based authentication




