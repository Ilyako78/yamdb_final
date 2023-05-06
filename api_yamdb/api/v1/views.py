from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api_yamdb.settings import DEFAULT_FROM_EMAIL

from .filters import TitleFilter
from .mixins import CreateListDestroyMixinSet
from .permissions import (AdministratorEdit, IsAdminOrModeratirOrAuthor,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateUserSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          SelfEditSerializer, TitleReadSerializer,
                          TitleWriteSerializer, UserSerialiser)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели user. Эндпойнт /users/* """
    queryset = User.objects.all()
    serializer_class = UserSerialiser
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (AdministratorEdit,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        serializer_class=SelfEditSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для регистрации пользователя"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email')
        ).exists():
            user = get_object_or_404(
                User,
                username=request.data.get('username')
            )
            response_data = request.data
        else:
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)
            response_data = serializer.data
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(response_data, status=status.HTTP_200_OK)


class GetTokenViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для валидации пользователя и передачи токена"""
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
                user,
                confirmation_code
        ) is False:
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class GenreViewSet(CreateListDestroyMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrModeratirOrAuthor]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    serializer_class = ReviewSerializer

    def title_query(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.title_query().id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_query())


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer

    def review_query(self):
        review = get_object_or_404(
            Review.objects.filter(title_id=self.kwargs.get('title_id')),
            pk=self.kwargs.get('review_id')
        )
        return review

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_query())
