# events/serializers.py
from django.db.models import Avg, Count
from .models import Event, UserInterest, EventRating, EventUser
from rest_framework import serializers


class EvenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUser
        fields = ['first_name', 'last_name', 'email', 'password', 'city']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = EventUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            city=validated_data['city'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class EventRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRating
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)
    city_member_rating = serializers.SerializerMethodField(read_only=True)
    interested_users_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'city', 'date', 'average_rating', 'city_member_rating',
                  'interested_users_count']

    def get_average_rating(self, event):
        return EventRating.objects.filter(event=event).aggregate(Avg("rating", default=0))

    def get_city_member_rating(self, event):
        request = self.context.get('request')
        curr_user_city = request.user.city
        return EventRating.objects.filter(event__city=curr_user_city).aggregate(Avg("rating", default=0))

    def get_interested_users_count(self, event):
        return UserInterest.objects.filter(event=event).count()
