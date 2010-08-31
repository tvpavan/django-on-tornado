Requirements
============
* Django_
* Tornado_

.. _Django: http://www.djangoproject.com/
.. _Tornado: http://www.tornadoweb.org/

Instructions
============

 1. ``cd myproject``
 3. ``python manage.py runtornado --reload``
 4. Go to: http://localhost:8000/

Now you have a working chat server -- this is based on the NodeJS chat server, UI primarily.

Quick Tutorial
==============

Django request/response is untouched.  To utilize Tornado's async capabilities, a decorator 
is avilable.  Which adds an extra argument to your request handler, which is the Tornado
handler class -- all functions are available.

If you return a value it is assumed to be a Django Response, if nothing is returned then
it is assumed that you're doing async response processing.

    from django_tornado.decorator import asynchronous

    @asynchronous
    def recv(request, handler) :
        response = {}

        if 'since' not in request.GET :
            return ChatResponseError('Must supply since parameter')
        if 'id' not in request.GET :
            return ChatResponseError('Must supply id parameter')

        id = request.GET['id']
        session = Session.get(id)
        if session :
            session.poke()

        since = int(request.GET['since'])

        def on_new_messages(messages) :
            if handler.request.connection.stream.closed():
                return
            handler.finish({ 'messages': messages, 'rss' : channel.size() })

        channel.query(handler.async_callback(on_new_messages), since)

Acknowledgements
================

Idea and code snippets borrowed from http://geekscrap.com/2010/02/integrate-tornado-in-django/
Chat server http://github.com/ry/node_chat
