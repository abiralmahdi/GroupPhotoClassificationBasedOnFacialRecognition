import os
import zipfile
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Event, PicsRelation, AnonymousUserPicsRelation
from accounts.models import User
from .serializers import PicsRelationSerializer
from .FacialRecognition import recognition  # Assuming recognition is defined in a utils module
from django.conf import settings


class CheckSimilarImagesAPI(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def post(self, request, user=None, event=None, mode="guest"):
        # Validate event existence
        event_ = get_object_or_404(Event, id=event)
        pics = PicsRelation.objects.filter(event=event_)
        relevant_pics = []

        # Validate user parameter
        userr = None
        if user is not None:
            try:
                userr = User.objects.get(id=user)
            except (User.DoesNotExist, ValueError):
                userr = None

        # Host mode: File upload and recognition
        if mode == "host":
            profilePic = request.FILES.get('uploadedPhoto')
            personName = request.data.get('personName', 'recognized_pics')

            if not profilePic:
                return Response({"error": "No photo uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            for pic in pics:
                image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                result = recognition(image_path, profilePic)
                if result:
                    relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                    if relevantPic:
                        AnonymousUserPicsRelation.objects.create(user=personName, image=relevantPic, event=event_)

            return Response({"message": "Recognition completed in host mode."}, status=status.HTTP_200_OK)

        # Guest mode
        elif mode == "guest":
            profilePic = None
            if userr:  # If a valid user object exists
                profilePic = userr.profilepicture
            if not profilePic:  # Check if uploaded photo is provided in the request
                profilePic = request.FILES.get('uploadedPhoto')

            if not profilePic:
                return Response({"error": "No profile picture provided."}, status=status.HTTP_400_BAD_REQUEST)

            for pic in pics:
                image_path = os.path.join(settings.MEDIA_ROOT, str(pic.image))
                result = recognition(image_path, profilePic)
                if result:
                    relevantPic = PicsRelation.objects.get(image=str(pic.image).replace('\\', '/'))
                    relevant_pics.append(image_path)
                    if relevantPic:
                        AnonymousUserPicsRelation.objects.create(user=request.user.username, image=relevantPic, event=event_)

            if relevant_pics:
                # Create a zip file for download
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file_path in relevant_pics:
                        zip_file.write(file_path, os.path.basename(file_path))
                zip_buffer.seek(0)

                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="YourPics.zip"'
                return response

            return Response({"message": "No matching pictures found."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid mode."}, status=status.HTTP_400_BAD_REQUEST)
