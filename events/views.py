# events/views.py
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Event, UserInterest, EventRating, EventUser
from .serializers import EventSerializer, UserInterestSerializer, EventRatingSerializer, EvenUserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class EventRegisterViewSet(viewsets.ModelViewSet):
    queryset = EventUser.objects.all()
    serializer_class = EvenUserSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventAuthViewSet(viewsets.ModelViewSet):
    queryset = EventUser.objects.all()
    serializer_class = EvenUserSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            user = None
            if '@' in email:
                try:
                    user = EventUser.objects.get(email=email)
                except ObjectDoesNotExist:
                    pass

            if not user:
                user = authenticate(username=email, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            # Delete the user's token to log out
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]


class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            'user': self.request.user.id,
            'event': request.data.get('event', None)
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventRateViewSet(viewsets.ModelViewSet):
    queryset = EventRating.objects.all()
    serializer_class = EventRatingSerializer
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            'user': self.request.user.id,
            'event': request.data.get('event', None),
            'rating': request.data.get('rating', None)
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
