from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from .models import UserTenantPermissions


class UserBackend(ModelBackend):
    """
    Authenticates against UserProfile 
    Authorizes against the UserTenantPermissions.
    The Facade classes handle the magic of passing
    requests to the right spot.
    """

    # We override this so that it looks for the 'groups' attribute on the 
    # UserTenantPermissions rather than from get_user_model() 
    def _get_group_permissions(self, user_obj):
        user_groups_field = UserTenantPermissions._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})


    # Clear any cached permissions for a user object. This is necessary
    # to call in any circumstance where a tenant is removed from a user
    # and lingering permissions are cached
    def clear_permissions_cache(self, user_obj):
        if hasattr(user_obj, '_perm_cache'):
            delattr(user_obj, '_perm_cache')

        if hasattr(user_obj, '_user_perm_cache'):
            delattr(user_obj, '_user_perm_cache')

        if hasattr(user_obj, '_group_perm_cache'):
            delattr(user_obj, '_group_perm_cache')
