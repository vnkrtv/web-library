# pylint: disable=import-error, no-else-return
"""
Decorators for differentiate user rights
"""
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    Checked if user is authorized
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return wrapper_func
