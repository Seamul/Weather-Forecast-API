from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TestModel


class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})

    def post(self, request):
        # {
        #     "message": "Hello, World!"
        # }
        request_data = request.data.copy()
        TestModel.objects.create(test_field=request_data['message'])
        return Response(request_data)
