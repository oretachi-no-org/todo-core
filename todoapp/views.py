from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from todoapp import serializers, models


class ListViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ListSerializer
    queryset = models.List.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super(ListViewSet, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        list_id = self.kwargs["list_id"]
        # Using double underscore to access foreign key
        # attribute list_id.
        return self.queryset.filter(list__list_id=list_id)

    def perform_create(self, serializer):
        serializer.save(list=models.List(list_id=self.kwargs["list_id"]))
