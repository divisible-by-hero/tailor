=================
Tailor Decorators
=================

@tailored
---------

Using the decorator ``@tailored`` on a fabric method will set an attribute that allows the method to be accessible via the tailor API.

Example::
    
    from tailor.decorators import tailored
    
    @tailored
    def collect_static():
        """ Collect static files, run before comitting call alpha or production first """
        virtualenv("python manage.py collectstatic --noinput --settings=settings.%s" % env.branch)
    