from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rest_status
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.account.services.login_service import UserLoginService
from apps.account.serializers import UserLoginSerializer

class UserLoginApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = UserLoginService(email=serializer.validated_data.get('email'),
                                   password=serializer.validated_data.get('password')
                                   )
        status, res = service.login()
        if status:
            return Response(data=res, status=rest_status.HTTP_200_OK)
        return Response(data=({'message': res}), status=rest_status.HTTP_400_BAD_REQUEST)

