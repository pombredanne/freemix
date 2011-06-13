from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from freemix.permissions import PermissionsRegistry

class OwnerListView(ListView):
    """A base view for filtering based on the 'owner' of a particular object.  For now, 'owner' is expected to be a
       username that maps to a Django User.
    """

    permission = None

    def get_queryset(self):
        owner = get_object_or_404(User, username=self.kwargs.get("owner"))
        list = self.model.objects.filter(owner=owner)
        if self.permission:
            list = list.filter(PermissionsRegistry.get_filter(self.permission, self.request.user))
        return list

    def get_context_data(self, **kwargs):
        kwargs = super(OwnerListView, self).get_context_data(**kwargs)
        kwargs["owner"] = get_object_or_404(User,
                                            username=self.kwargs.get("owner"))
        kwargs["user"] = self.request.user
        return kwargs


class OwnerSlugDetailView(DetailView):

    def filter_by_perm(self, obj):
        if hasattr(self, "object_perm") and \
            not self.request.user.has_perm(getattr(self, "object_perm"), obj):
                raise Http404
        return obj


    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                 owner__username=self.kwargs.get("owner"),
                                 slug=self.kwargs.get("slug"))
        return self.filter_by_perm(obj)
