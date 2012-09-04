=================
Tailor Decorators
=================

@tailored
---------

Using the decorator ``@tailored`` on a fabric method will set an attribute that allows the method to be accessible via the tailor API.

Example::
    
    from tailor.client.decorators import tailored
    
    @tailored
    def collect_static():
        """ Collect static files, run before comitting call alpha or production first """
        virtualenv("python manage.py collectstatic --noinput --settings=settings.%s" % env.branch)
    
    
@dependency
-----------

The dependency decorator is used when Tailor needs access to the fabric command for the API, but you don't want to be able to access the method directly.


Example::

    from tailor.client.decorators import dependency
    
    @dependency
    def virtualenv(command):
        with cd(env.directory):
            run(env.activate + '&&' + command)