from rest_framework import serializers
from .models import Livro,Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='category_name')
    class Meta:
        model = Category
        fields = ["id",'slug','title']

class LivroSerializer(serializers.ModelSerializer):
    disponiveis = serializers.IntegerField(source='quantidade')
    preco_com_taxa = serializers.SerializerMethodField(method_name='taxa_governo')
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Livro
        fields = ["id",'nome','autor','descricao','price','disponiveis','preco_com_taxa','category','category_id']
        extra_kwargs= {
            'price': {'min_value': 1},
            'disponiveis': {'min_value': 0}
        }
        
    def taxa_governo(self,produto:Livro):
        return produto.price * Decimal(1.1)