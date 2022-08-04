from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from my_game_list import __version__


class ApiVersion(APIView):
    """Endpoint for the version of the application."""
    def get(self, request: Request, *args, **kwargs):
        version = ".".join(map(str, __version__))
        return Response(version)
