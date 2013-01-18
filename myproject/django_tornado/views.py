# Create your views here.

from django.core.handlers.wsgi import STATUS_CODE_TEXT

def djtor_view_response(request,response):
    handler = request._tornado_handler
    # Apply response middleware
    for middleware_method in handler._response_middleware:
        response = middleware_method(request, response)
    response = handler.apply_response_fixes(request, response)
    #finally:
    #signals.request_finished.send(sender=handler.__class__)
    
    try:
        status_text = STATUS_CODE_TEXT[response.status_code]
    except KeyError:
        status_text = 'UNKNOWN STATUS CODE'
    status = '%s %s' % (response.status_code, status_text)
    
    handler.set_status(response.status_code)
    for h in response.items() :
        handler.set_header(h[0], h[1])
    
    for c in response.cookies.values():
        handler.set_header('Set-Cookie', str(c.output(header='')))
    
    """
    if  hasattr(handler, "_new_cookies"):
        print handler._new_cookies
    handler._new_cookies = response.cookies
    """
    
    handler.write(response.content)
    handler.finish()
