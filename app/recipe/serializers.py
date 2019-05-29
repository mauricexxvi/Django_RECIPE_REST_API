from rest_framework import serializers
from core.models import Step, Ingredient, Recipe


class StepSerializer(serializers.ModelSerializer):
    """Serializer for step objects"""
    model = Step
    fields = ('id', 'name')
    read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Step.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes', 'price',
            'link',
        )
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)