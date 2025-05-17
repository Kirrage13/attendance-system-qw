from django.http import HttpRequest, HttpResponse


def set_useragent_or_request_middleware(get_response):

    def middleware(request: HttpRequest):
        request.user_agent = request.META.get("HTTP_USER_AGENT", "")
        response = get_response(request)
        return response

    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.responses_count = 0
        self.exeptions_count = 0

    def __call__(self, request: HttpRequest):
        self.request_count += 1
        print("request count", self.request_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exeptions_count += 1
        print("got", self.exeptions_count, "exceptions so far")
