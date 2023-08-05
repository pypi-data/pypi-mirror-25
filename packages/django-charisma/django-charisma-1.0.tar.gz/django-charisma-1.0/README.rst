=====
Charisma Django
=====

Charisma Django is a port from charisma template from Usman.

It is free, responsive, multiple skin admin template.

Detailed documentation is in the "docs" directory.

Live demo <https://grrodre.com/django-charisma/live/>


Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
    'charisma_django',
    ]

2. Include the polls URLconf in your project urls.py like this::
    
    url(r'^', include('charisma_django.urls')),

3. Run `python manage.py migrate` to create the charisma models.

4. Start the development server and visit http://127.0.0.1:8000/

5. Create your own boxes and adapt the template for your needs.
