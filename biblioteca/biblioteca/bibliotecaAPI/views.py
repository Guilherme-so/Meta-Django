# from rest_framework import generics
# from .models import Livro,Category
# from .serializers import LivroSerializer,CategorySerializer
# from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# class LivrosView(generics.ListCreateAPIView):
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#     queryset = Livro.objects.all()
#     serializer_class = LivroSerializer
#     ordering_fields = ['price', 'quantidade']
#     filterset_fields = ['price', 'quantidade']
#     search_fields = ['nome']

# class SingleLivroView(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
#     queryset =  Livro.objects.all()
#     serializer_class = LivroSerializer
    
    
# class CategoriesView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     search_fields = ['category_name']


# class SingleCategory(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# ---------------------------------------------------------------------------------------------------------------------

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes, throttle_classes
from .serializers import LivroSerializer,CategorySerializer
from rest_framework.response import Response
from .models import Livro,Category
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import FiveCallsPerMinute

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([FiveCallsPerMinute])
def livros(request):
    if request.method == "GET":
        items  = Livro.objects.all()
        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        page = request.query_params.get('page', default=1)
        perpage = request.query_params.get('perpage', default=10)
        
        if(category_name):
            items = items.filter(category__category_name=category_name)
        if(price):
            items = items.filter(price__lte=price)
        if(search):
            items = items.filter(nome__istartswith=search)
        if(ordering):
            # items = items.order_by(ordering)
            ordering_many = ordering.split(',')
            items = items.order_by(*ordering_many)
            
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
            
        serialized_item = LivroSerializer(items, many=True)
        return Response(serialized_item.data)
    
    
    if request.method == "POST":
        serialized_item = LivroSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def livro(request, pk):
    item = get_object_or_404(Livro, pk=pk)

    if request.method == "GET":
        serilized_item = LivroSerializer(item)
        return Response(serilized_item.data)
    
    elif request.method == "PUT":
        serilized_item = LivroSerializer(item,data=request.data)
        serilized_item.is_valid(raise_exception=True)
        serilized_item.save()
        return Response(serilized_item.data,status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        item.delete()
        return Response({'message': "Item apagado com successo!"})

@api_view(['GET','POST'])
def categories(request):
    if request.method == "GET":
        items = Category.objects.all()
        item_serialized = CategorySerializer(items, many=True)
        return Response(item_serialized.data)

    if request.method == "POST":
        item_serialized = CategorySerializer(data=request.data)
        item_serialized.is_valid(raise_exception=True)
        item_serialized.save()
        return Response(item_serialized.data, status.HTTP_201_CREATED)


@api_view(["GET","PUT","DELETE"])
def singleCategory(request, id):
    item = get_object_or_404(Category,pk=id)
        
    if(request.method == "GET"):
        item_serialized = CategorySerializer(item)
        return Response(item_serialized.data)
    
    elif(request.method == "PUT"):
        item_serialized = CategorySerializer(item, data=request.data)
        item_serialized.is_valid(raise_exception=True)
        item_serialized.save()
        return Response(item_serialized.data, status.HTTP_200_OK)
    
    elif(request.method == "DELETE"):
        item.delete()
        return Response({"message": "Categoria apagada com successo."}, status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAdminUser])
def aluguel(request):
    usuario = request.data['usuario']
    if(usuario):
        user = get_object_or_404(User, username=usuario)
        aluguel_grupo = Group.objects.get(name="Aluguel")
        if request.method == "POST":
            aluguel_grupo.user_set.add(user)
        if request.method == "DELETE":
            aluguel_grupo.user_set.remove(usuario)

        return Response({'message': "Adicionado ao grupo de aluguel"}, status.HTTP_201_CREATED)
    
    return Response({'message':'Voce nao tem autorizacao para fazer isso.'}, status.HTTP_401_UNAUTHORIZED) 