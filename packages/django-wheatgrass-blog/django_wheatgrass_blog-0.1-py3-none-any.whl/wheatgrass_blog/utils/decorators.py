from django.core.exceptions import PermissionDenied

def admin_required(view):
    '''Checks if a user is an admin.

    Returns an HTTP 403 error if not.
    '''
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        else:
            return view(request, *args, **kwargs)
    return wrapper
