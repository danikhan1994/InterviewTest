from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import App, Subscription
from .serializers import AppSerializer, SubscriptionSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def registerUser(request):
    user = UserSerializer(data=request.data)

    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This user already exists')

    if user.is_valid():
        User.objects.create_user(
            email=request.data['email'],
            username=request.data['username'],
            password=request.data['password'],
            is_staff=request.data['is_staff'],
            is_superuser=request.data['is_superuser']
        )
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def loginUser(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getApps(request):
    apps = App.objects.all()
    serializer = AppSerializer(apps, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createApp(request):
    user = User.objects.get(pk=request.user.id)
    new_app = App.objects.create(
        name=request.data['name'],
        description=request.data['description'],
        user=user
    )
    get_app = App.objects.get(pk=new_app.id)
    subscribe = Subscription.objects.create(app=get_app, subscribed=True)
    subscribe.save()
    serializer = AppSerializer(instance=get_app)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateApp(request, pk):
    update_app = App.objects.filter(pk=pk).update(
        name=request.data['name'],
        description=request.data['description']
    )
    find = App.objects.get(pk=pk)
    app = AppSerializer(find, many=False)
    return Response(app.data)
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteApp(request, pk):
    app = get_object_or_404(App, pk=pk)
    app.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSubscriptions(request):
    subs = Subscription.objects.all()
    serializer = SubscriptionSerializer(subs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateSubscription(request):
    update = Subscription.objects.filter(app=request.data['app']).update(
        plan=request.data['plan'],
        subscribed=request.data['subscribed']
    )
    find = Subscription.objects.get(app=request.data['app'])
    subs = SubscriptionSerializer(find, many=False)
    return Response(subs.data)