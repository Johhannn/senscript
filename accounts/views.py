from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics
from .serializers import ProfileSerializer
from .pagination import ProfilePagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Project
from .serializers import ProjectSerializer
from django.http import Http404


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination


@api_view(['GET'])
def get_projects_for_profile(request, profile_id):
    try:
        profile = Profile.objects.get(id=profile_id)

        projects = Project.objects.filter(profile=profile)

        if not projects:
            return Response({"message": "No projects found for this profile."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        raise Http404("Profile not found")