#Tailor
Tailor is a Django app that let's you run Fabric commands via a web based API.

###Running Tailor on a seperate host
Optimally, Tailor should be installed on different host than the target host.  In other words, a project running Tailor on Host1 will execute Fabric commands on Host2.

###Running Tailor on the same host
Tailor can also run on the same host you want to run Fabric commands on.  However, caution must be exercised or Tailor could cause some funky behavior. For example, if a Fabric command deleted the very project running Tailor.

#Docs
Check out the full documentation.

http://readthedocs.org/docs/tailor/en/latest/