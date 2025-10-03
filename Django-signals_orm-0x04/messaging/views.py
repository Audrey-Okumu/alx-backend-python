#a simple view that deletes the currently logged-in user.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their account.
    """
    user = request.user
    user.delete()   # triggers post_delete signal
    return redirect('/')  # redirect to homepage after deletion
