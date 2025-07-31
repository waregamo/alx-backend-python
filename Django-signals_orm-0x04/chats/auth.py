from rest_framework import views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginUserSerializer, RegisterUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Handle user registration logic
class RegisterUserView(views.APIView):
    def post(self, request):
        # Initialize the serializer with the provided request data
        serializer = RegisterUserSerializer(data=request.data)
        
        # Check if the data is valid according to the serializer's validation logic
        if serializer.is_valid():
            # Save the new user to the database if the data is valid
            serializer.save()
            
            # Return a success message with HTTP status 201 (Created)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        # If the serializer data is invalid, return the validation errors with HTTP status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handle user login logic
class LoginUserView(views.APIView):
    def post(self, request):
        # Initialize the login serializer with the provided request data
        serializer = LoginUserSerializer(data=request.data)

        # Check for data validation
        if not serializer.is_valid():
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
    
        user_email = serializer.validated_data['email']
        user_password = serializer.validated_data['password']
    
        # Attempt to authenticate the user
        try:
            user = User.objects.get(email=user_email)
            user_data = {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            if user.check_password(user_password):
                # Create JWT token
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                # Return the tokens
                return Response({'user_data':user_data,'access': str(access_token),'refresh': str(refresh)})
            return Response({"error": "Invalid password!"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Invalid email!"}, status=status.HTTP_400_BAD_REQUEST)