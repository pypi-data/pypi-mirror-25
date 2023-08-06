from django.views import debug
from django.conf import settings
from .exceptions import (ImProperTypeError, ImProperValueError)


# Middleware class follows
class DjangoErrorAssistMiddleware(object):
    def __init__(self, get_response):
        """
        Middleware to get the help for the error that occurs in Django from
        source developers prefer.
        """
        # https://docs.djangoproject.com/en/1.11/topics/http/middleware/#writing-your-own-middleware
        self.get_response = get_response
        if settings.DEBUG:
            # dict of URLs
            self.sources = dict()
            self.sources['stackoverflow'] = "http://stackoverflow.com/search?q=python+or+django+"
            self.sources['google'] = "https://www.google.co.in/#q=django "

            self.__REPLACE_STRING = '<th>Exception Type:</th>'
            self.__HTML_STRING = """
            <h3 class="DjangoErrorAssist">
                <a href="%s" target="_blank">Get assist for this error in %s 
                </a>
            <h3>
            """
            self.__set_source_for_online_help()
            # calling the method to edit the django template
            self._alter_django_500_debug_template()
            # calling the method to stdout the error

    def __call__(self, request):
        return self.get_response(request)

    def __set_source_for_online_help(self):
        # check for user's preference of source from settings file
        if getattr(settings, 'DJANGO_ERROR_ASSIST_FROM', None):
            # check if the variable has been set to right 'type'
            if not isinstance(settings.DJANGO_ERROR_ASSIST_FROM, str):
                raise ImProperTypeError("DJANGO_ERROR_ASSIST_FROM variable "
                                        "should be of type 'str' ")
            # check if the variable is valid and expected string
            if settings.DJANGO_ERROR_ASSIST_FROM.lower() not in self.sources.iterkeys():
                raise ImProperValueError("DJANGO_ERROR_ASSIST_FROM variable can take either "
                                         "'google' or 'stackoverflow' ")
        else:
            setattr(settings, 'DJANGO_ERROR_ASSIST_FROM', 'stackoverflow')

        # get the URL link for the selected source
        self.query_link = self.sources.get(settings.DJANGO_ERROR_ASSIST_FROM)

    def _alter_django_500_debug_template(self):
        # append the exception type to the query link
        self.query_link += "{{ exception_type|escape }}"
        # append the query_link to HTML_STRING
        self.formatted_html_string = self.__HTML_STRING % (self.query_link,
                                                      settings.DJANGO_ERROR_ASSIST_FROM)
        # get the replacement string
        replacement = self.__REPLACE_STRING + self.formatted_html_string
        # check if this class exists in the template
        if "DjangoErrorAssist" not in debug.TECHNICAL_500_TEMPLATE:
            # patch up the built-in template with custom html string
            debug.TECHNICAL_500_TEMPLATE = \
                debug.TECHNICAL_500_TEMPLATE.replace(self.__REPLACE_STRING,
                                                     replacement)
