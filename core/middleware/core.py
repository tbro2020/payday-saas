
class CoreMiddleware:
    MAX_AGE = 30*24*60*60
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        response.set_cookie('visited', False, max_age=self.MAX_AGE)
        return response