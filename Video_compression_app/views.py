from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from Video_compression_app import serializers
from Video_compression_app.models import Video
from django.http import FileResponse
import subprocess
import os


class VideoCompressionView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = serializers.VideoSerializer(data=request.data)
        if serializer.is_valid():
            video_file = serializer.validated_data['video_file']
            size_limit = serializer.validated_data['size_limit']

            # Define the path for the compressed video in the current directory
            compressed_video_filename = 'compressed_video.mp4'
            compressed_video_path = os.path.join(os.getcwd(), compressed_video_filename)

            # Define initial compression parameters
            current_bitrate = 1500 # Initial bitrate in kbps
            step = 100 # Step for bitrate adjustment

            while True:
                # Construct the FFmpeg command with the current bitrate
                compression_command = f'ffmpeg -i "{video_file.temporary_file_path()}" -b:v {current_bitrate}k -strict experimental -vf scale=1280:-2 -y "{compressed_video_path}"'

                # Execute the FFmpeg command for video compression
                subprocess.run(compression_command, shell=True)

                # Get the size of the compressed video
                compressed_size = os.path.getsize(compressed_video_path)

                def parse_size_limit(self, size_limit):
                    size_limit = size_limit.strip().lower()
                    if size_limit.endswith('kb'):
                        return int(size_limit[:-2]) * 1024
                    elif size_limit.endswith('mb'):
                        return int(size_limit[:-2]) * 1024 ** 2
                    elif size_limit.endswith('gb'):
                        return int(size_limit[:-2]) * 1024 ** 3
                    return int(size_limit)

                # Check if the size is within the target limit
                if compressed_size <= parse_size_limit(self,size_limit):
                    break  # The compressed video size is within the limit
                else:
                    # Reduce the bitrate if the size is larger than the limit
                    current_bitrate -= step
                    if current_bitrate <= 0:
                        break  # Ensure we don't go below 0 bitrate

            # Return the compressed video as an attachment
            with open(compressed_video_path, 'rb') as video_file:
                response = FileResponse(video_file)
                response['Content-Disposition'] = f'attachment; filename="{compressed_video_filename}"'
                return response

        return Response(serializer.errors)


