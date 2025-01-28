from rest_framework.permissions import BasePermission
from uuid import UUID


class OnlyWalletOwnerWithOutBodyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.id == request.__dict__["parser_context"]["kwargs"]["user_id"]:
                return True
            return False
        return False


class OnlyWalletOwnerWithBodyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.id == UUID(request.data.get("user_id")):
                return True
            return False
        return False
