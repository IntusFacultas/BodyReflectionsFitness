from django.core.urlresolvers import resolve


class DisableCSRF(object):
    """Middleware for disabling CSRF in an specified app name.
    """

    def process_request(self, request):
        """Preprocess the request.
        """
        print('active')
        setattr(request, '_dont_enforce_csrf_checks', True)
        # app_name = "api"
        # if resolve(request.path_info).app_name == app_name:
        # else:
        #     pass  # check CSRF token validation
