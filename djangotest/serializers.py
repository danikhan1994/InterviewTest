from rest_framework import serializers
from django.contrib.auth.models import User
from .models import App, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AppSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = App
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    app = serializers.ReadOnlyField(source='app.name')
    plan = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = '__all__'
    
    def get_plan(self, obj):
        if obj.plan == 1:
            return 'Free ($0)'
        elif obj.plan == 2:
            return 'Standard ($10)'
        elif obj.plan == 3:
            return 'Pro ($25)'