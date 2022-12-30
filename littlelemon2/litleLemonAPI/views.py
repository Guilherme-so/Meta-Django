from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, throttle_classes
from .models import MenuItem,Category
from .serializers import MenuItemSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

#Paginations
from django.core.paginator import Paginator, EmptyPage
#Auth
from rest_framework.permissions import IsAuthenticated
#Throttle
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute, TwentyCallsPerMinute, TwentyCallsPerDay

from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group,User

# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def CategoryView(request):
        if(request.method == "GET"):
            category = Category.objects.all()
            serializeCategory = CategorySerializer(category, many=True)            
            return Response(serializeCategory.data)
        
        if(request.method =="POST"):
            serialized_category = CategorySerializer(data=request.data)
            serialized_category.is_valid(raise_exception=True)
            serialized_category.save()
            return Response(serialized_category.validated_data, status.HTTP_201_CREATED)
        

@api_view(['GET','POST'])
@throttle_classes([AnonRateThrottle])
def MenuItems(request):
    if(request.method == "GET"):
        items = MenuItem.objects.all()
        
        # filtro e search variaveis
        category_name = request.query_params.get('category')        #   /api/menu-items?category=drink
        price = request.query_params.get('price')                   #  /api/menu-items?price=20
        search = request.query_params.get('search')                 #  /api/menu-items?search=coca
        ordering = request.query_params.get('ordering')             #  /api/menu-items?ordering=price ou id 
        
        #pagination
        perpage = request.query_params.get("perpage", default=2)    # items por pagina
        page = request.query_params.get('page', default=1)          # pagina
                                                                    # /api/menu-items?perpage=4&page=1
        
        
        # filtro, search e ordenaçao logica
        if(category_name):
            #filtrar por categoria
            items = items.filter(category__title = category_name)
        if(price):
            #filtrar por preco
            items = items.filter(price__lte = price)
        if(search):
            # search field
            items = items.filter(title__istartswith = search)
            # items = items.filter(title__icontains = search)
        if(ordering):
            items = items.order_by(ordering)
            #organizar com 2 campos
            # orderiing_fields = ordering.split(",")
            # items = items.order_by(*orderiing_fields)
        
        #pagination logica
        pagination = Paginator(items, per_page=perpage)
        try:
            items = pagination.page(number=page)
        except EmptyPage:
            items = []
            
        serialize_items = MenuItemSerializer(items, many=True)
        return Response(serialize_items.data)
    
    elif(request.method == "POST"):
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
    
    
    
@api_view()
@permission_classes([IsAuthenticated])
def Secret(request):
    return Response({'message': 'some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def menager(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"Message": "Just Menager SHould see this"})
    else:
        return Response({'Message': 'Your Are not Allowed to see this'}, status.HTTP_403_FORBIDDEN)
    
    
# limitar o acesso para anonimos 
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"Message": "Success"})


# limitar o acesso para authenticados
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TwentyCallsPerDay]) #ou UserRateThrottle,TenCallsPerMinute,TwentyCallsPerMinute
def throttle_check_auth(request):
    return Response({'Message': 'Message For the logged in users only'})

#adicionar e remover users do group de manager
@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == "POST":
            managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.delete(user)
            
        return Response({'message': 'ok'})
    
    return Response({'message': 'error'}, status.HTTP_400_BAD_REQUEST)