# -*- coding: utf-8 -*-
"""
Decorators for enterprise app.
"""
from __future__ import absolute_import, unicode_literals

import inspect
import warnings
from functools import wraps

from requests.utils import quote

from django.http import Http404
from django.shortcuts import redirect

from enterprise.utils import get_enterprise_customer_or_404, get_identity_provider
from six.moves.urllib.parse import parse_qs, urlencode, urlparse, urlunparse  # pylint: disable=import-error


def deprecated(extra):
    """
    Flag a method as deprecated.

    :param extra: Extra text you'd like to display after the default text.
    """
    def decorator(func):
        """
        Return a decorated function that emits a deprecation warning on use.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrap the function.
            """
            message = 'You called the deprecated function `{function}`. {extra}'.format(
                function=func.__name__,
                extra=extra
            )
            frame = inspect.currentframe().f_back
            warnings.warn_explicit(
                message,
                category=DeprecationWarning,
                filename=inspect.getfile(frame.f_code),
                lineno=frame.f_lineno
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def ignore_warning(warning):
    """
    Ignore any emitted warnings from a function.

    :param warning: The category of warning to ignore.
    """
    def decorator(func):
        """
        Return a decorated function whose emitted warnings are ignored.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrap the function.
            """
            warnings.simplefilter('ignore', warning)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def disable_for_loaddata(signal_handler):
    """
    Use this decorator to turn off signal handlers when loading fixture data.

    Django docs instruct to avoid further changes to the DB if raw=True as it might not be in a consistent state.
    See https://docs.djangoproject.com/en/dev/ref/signals/#post-save
    """
    # http://stackoverflow.com/a/15625121/882918
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        """
        Wrap the function.
        """
        if kwargs.get('raw', False):
            return
        signal_handler(*args, **kwargs)
    return wrapper


def enterprise_login_required(view):
    """
    View decorator for allowing authenticated user with valid enterprise UUID.

    This decorator requires enterprise identifier as a parameter
    `enterprise_uuid`.

    This decorator will throw 404 if no kwarg `enterprise_uuid` is provided to
    the decorated view .

    If there is no enterprise in database against the kwarg `enterprise_uuid`
    or if the user is not authenticated then it will redirect the user to the
    enterprise-linked SSO login page.

    Usage::
        @enterprise_login_required()
        def my_view(request, enterprise_uuid):
            # Some functionality ...

        OR

        class MyView(View):
            ...
            @method_decorator(enterprise_login_required)
            def get(self, request, enterprise_uuid):
                # Some functionality ...

    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        """
        Wrap the decorator.
        """
        if 'enterprise_uuid' not in kwargs:
            raise Http404

        enterprise_uuid = kwargs['enterprise_uuid']
        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)

        # Now verify if the user is logged in. If user is not logged in then
        # send the user to the login screen to sign in with an
        # Enterprise-linked IdP and the pipeline will get them back here.
        if not request.user.is_authenticated():
            parsed_current_url = urlparse(request.get_full_path())
            parsed_query_string = parse_qs(parsed_current_url.query)
            parsed_query_string.update({'tpa_hint': enterprise_customer.identity_provider})
            next_url = '{current_path}?{query_string}'.format(
                current_path=quote(parsed_current_url.path),
                query_string=urlencode(parsed_query_string)
            )
            return redirect(
                '{login_url}?{params}'.format(
                    login_url='/login',
                    params=urlencode(
                        {'next': next_url}
                    )
                )
            )

        # Otherwise, they can proceed to the original view.
        return view(request, *args, **kwargs)

    return wrapper


def force_fresh_session(view):
    """
    View decorator which terminates stale TPA sessions.

    This decorator forces the user to obtain a new session
    the first time they access the decorated view. This prevents
    TPA-authenticated users from hijacking the session of another
    user who may have been previously logged in using the same
    browser window.

    This decorator should be used in conjunction with the
    enterprise_login_required decorator.

    Usage::
        @force_fresh_session()
        def my_view(request, enterprise_uuid):
            # Some functionality ...

        OR

        class MyView(View):
            ...
            @method_decorator(force_fresh_session)
            def get(self, request, enterprise_uuid):
                # Some functionality ...

    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        """
        Wrap the function.
        """
        if not request.session.get('is_session_fresh'):
            if request.user.is_authenticated():
                # If the user is logged in, the sso provider is configured
                # to terminate existing sessions, and we have not yet
                # restarted the session, redirect the user to the logout
                # page to terminate the session and include a redirect URL
                # which will send them back to the original view so they
                # can start a new session.
                enterprise_customer = get_enterprise_customer_or_404(kwargs.get('enterprise_uuid'))
                provider_id = enterprise_customer.identity_provider or ''

                try:
                    sso_provider = get_identity_provider(provider_id)
                    if sso_provider and sso_provider.drop_existing_session:
                        # Parse the current request full path, quote just the path portion,
                        # then reconstruct the full path string.
                        # The path and query portions should be the only non-empty strings here.
                        scheme, netloc, path, params, query, fragment = urlparse(request.get_full_path())
                        redirect_url = urlunparse((scheme, netloc, quote(path), params, query, fragment))

                        return redirect(
                            '{logout_url}?{params}'.format(
                                logout_url='/logout',
                                params=urlencode(
                                    {'redirect_url': redirect_url}
                                )
                            )
                        )
                except ValueError:
                    pass
            else:
                # If the user has not yet been authenticated,
                # set a flag on the session to indicate that
                # this is a fresh session.
                request.session['is_session_fresh'] = True

        else:
            # The user was forced to log out and start a new session,
            # so clear the session flag.
            request.session.pop('is_session_fresh')

        return view(request, *args, **kwargs)

    return wrapper
