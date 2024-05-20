from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):

    if request.method == 'GET':
        try:
            # verifica se existe o parâmetro user (/?user=xxx)
            if 'user' in request.GET:
                user_nickname = request.GET['user']
                try:
                    user = User.objects.get(pk=user_nickname)
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

            elif 'all' in request.GET:
                try:
                    users = User.objects.all()
                    serializer = UserSerializer(users, many=True)
                    return Response(serializer.data)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        try:

            if 'create' in request.GET:

                user_data = {
                    "user_nickname": request.data.get('user_nickname'),
                    "user_name": request.data.get('user_name'),
                    "user_email": request.data.get('user_email'),
                    "user_age": request.data.get('user_age')
                }

                user = User(**user_data)

                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            if 'update' in request.GET:
                user_id = request.data.get('id')
                user = User.objects.get(id=user_id)

                user.user_nickname = request.data.get('user_nickname', user.user_nickname)
                user.user_name = request.data.get('user_name', user.user_name)
                user.user_email = request.data.get('user_email', user.user_email)
                user.user_age = request.data.get('user_age', user.user_age)

                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            Response(status=status.HTTP_400_BAD_REQUEST)


# GET ALL
@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':
        users = User.objects.all()  # BUSCAR TODOS
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# GET ONE
@api_view(['GET'])
def get_by_nick(request, nick):

    try:
        user = User.objects.get(pk=nick)  # BUSCAR UM
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

# GET ON (BODY REQUEST)


@api_view(['POST'])
def get_by_nick_by_body(request):
    nick = request.data.get('nick')  # PEGANDO NICK DO BODY DA REQUISIÇÃO

    if not nick:
        return Response({'error': 'Nick is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(pk=nick)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


# FILTRAR TODOS COM IDADE MAIOR QUE AGE
@api_view(['GET'])
def get_by_age_more_than(request, age):
    if request.method == 'GET':
        try:
            age = int(age)
            # LT = USADO PARA FILTRAR (MAIOR)
            users = User.objects.filter(user_age__gt=age)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Age must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# FILTRAR TODOS COM IDADE MENOR QUE AGE
@api_view(['GET'])
def get_by_age_under_than(request, age):
    if request.method == 'GET':
        try:
            age = int(age)
            # LT = USADO PARA FILTRAR (MENOR)
            users = User.objects.filter(user_age__lt=age)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Age must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# def databaseEmDjango():
#     data = User.objects.get() #retorna um objeto

#     data = User.objects.filter() #retorna uma queryset

#     data = User.objects.exclude() #retorna uma queryset

#     data.save()
#     data.delete()
