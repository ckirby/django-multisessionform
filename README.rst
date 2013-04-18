Django Multi Session Form
=========================

Allows interaction with a form over multiple sessions, similar to many job and school application sites.

::

    $ pip install django-multi-session-form
	
or download from github (http://github.com/ckirby/django-multi-session-form)

::

    $ python setup.py install
	
The project provides a mixin that will add the following methods to a model:

* class methods:

 * get\_required\_fields()
 * multisessionform\_factory()
 
* instance methods:

 * is\_complete()
 * get\_firs\t_incomplete\_field()
 * complete\_fields(ignore_required_fields = True)
 * incomplete\_fields()
 
