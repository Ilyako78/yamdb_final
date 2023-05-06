from rest_framework import mixins, viewsets


class CreateListDestroyMixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
