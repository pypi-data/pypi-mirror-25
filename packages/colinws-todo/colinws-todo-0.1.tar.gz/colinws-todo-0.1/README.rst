=====
Django Todo List
=====

Todo is a simple Django app to conduct Web-based todo list. 
You can add your new list to do and check for some which had beed finished, 
or recover the finished to un-finished status.
or you can delete items

Detailed documentation is in the "docs" directory.


Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'todo',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^todo/', include('todo.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/todo/ to participate in the poll.
