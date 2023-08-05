import datetime

from django.conf import settings

from cache_headers.utils import httpdate


try:
    browser_cache_seconds = settings.CACHE_HEADERS["browser-cache-seconds"]
except (KeyError, AttributeError):
    browser_cache_seconds = 5


def all_users(request, response, user, age):
    """Content is cached once for all users."""

    response["Last-Modified"] = httpdate(datetime.datetime.utcnow())
    # nginx specific but safe to set in all cases
    response["X-Accel-Expires"] = age
    response["Cache-Control"] = "max-age=%d, s-maxage=%d" \
        % (browser_cache_seconds, age)
    response["X-Hash-Cookies"] = "messages"
    response["Vary"] = "Accept-Encoding,Cookie"


def anonymous_only(request, response, user, age):
    """Content is cached once only for anonymous users."""

    if user.is_anonymous():
        response["Last-Modified"] = httpdate(datetime.datetime.utcnow())
        # nginx specific but safe to set in all cases
        response["X-Accel-Expires"] = age
        response["Cache-Control"] = "max-age=%d, s-maxage=%d" \
            % (browser_cache_seconds, age)
        response["X-Hash-Cookies"] = "messages"
        response["Vary"] = "Accept-Encoding,Cookie"
    else:
        response["Cache-Control"] = "no-cache"


def anonymous_and_authenticated(request, response, user, age):
    """Content is cached once for anonymous users and once for authenticated
    users."""

    response["Last-Modified"] = httpdate(datetime.datetime.utcnow())
    # nginx specific but safe to set in all cases
    response["X-Accel-Expires"] = age
    response["Cache-Control"] = "max-age=%d, s-maxage=%d" \
        % (browser_cache_seconds, age)
    response["X-Hash-Cookies"] = "messages|isauthenticated"
    response["Vary"] = "Accept-Encoding,Cookie"


def per_user(request, response, user, age):
    """Content is cached once for anonymous users and for each authenticated
    user individually."""

    response["Last-Modified"] = httpdate(datetime.datetime.utcnow())
    # nginx specific but safe to set in all cases
    response["X-Accel-Expires"] = age
    response["Cache-Control"] = "max-age=%d, s-maxage=%d" \
        % (browser_cache_seconds, age)
    response["X-Hash-Cookies"] = "messages|sessionid"
    response["Vary"] = "Accept-Encoding,Cookie"
