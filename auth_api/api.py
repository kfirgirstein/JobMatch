
from django.contrib.auth import authenticate,login, logout
from rest_framework import status,views
from rest_framework.response import Response
from app.serializers import UserSerializer

class LoginView(views.APIView):

    def post(self,request):
        username_res=request.data.get("username")
        password_res=request.data.get("password")
        user_answer = authenticate(username=username_res, password=password_res)

        if user_answer is None or not user_answer.is_active:
            return Response({
                    'status':'Unauthenticate',
                    'message':'username orpassword incorrect'
                },status=status.HTTP_401_UNAUTHORIZED)
        login(request,user_answer)
        return Response(UserSerializer(user_answer).data)

class LogoutView(views.APIView):

    def get(self,request):
        logout(request)
        return Response({},status=status.HTTP_204_NO_CONTENT)

class IsLoogedIntView(views.APIView):
    def get(self,request):
            return Response(request.user.is_authenticated())

        


