from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from .models import CustomUser, StoredJWT, Message, Like, Review
from store.models import Store
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    MessageSerializer,
    LikeSerializer,
    ReviewSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserProfileSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """
        Get or update the user's profile
        """
        if request.method == 'GET':
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        
        # Handle profile updates
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """
        Endpoint to handle email verification
        """
        # Add your email verification logic here
        pass

    @action(detail=False, methods=['post'])
    def verify_phone(self, request):
        """
        Endpoint to handle phone verification
        """
        # Add your phone verification logic here
        pass

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)
        refresh.payload["username"] = user.username

        # Check if the user owns a store and add the store_id to the token
        try:
            store = Store.objects.get(owner=user)
            refresh.payload["store_id"] = store.id
            refresh.payload["is_merchant"] = True
        except Store.DoesNotExist:
            refresh.payload["store_id"] = None
            refresh.payload["is_merchant"] = False

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        StoredJWT.objects.update_or_create(
            user=user,
            defaults={'access_token': access_token, 'refresh_token': refresh_token}
        )

        # Include basic user info in response
        return Response({
            "access": access_token,
            "refresh": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "has_store": refresh.payload["store_id"] is not None
            }
        })

# Keep other views as they are
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        StoredJWT.objects.filter(user=user).delete()
        logout(request)
        return Response({"message": "Logged out successfully"})

class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        stored_jwt = StoredJWT.objects.filter(user=user).first()
        
        if not stored_jwt:
            return Response({"error": "No valid refresh token found"}, status=400)
        
        try:
            refresh = RefreshToken(stored_jwt.refresh_token)
            access_token = str(refresh.access_token)
            
            stored_jwt.access_token = access_token
            stored_jwt.save()

            return Response({"access": access_token})
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=400)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)
 