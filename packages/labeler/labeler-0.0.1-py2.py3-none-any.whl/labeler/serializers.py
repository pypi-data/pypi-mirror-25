from rest_framework import serializers
from labeler.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CustomeImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    caption = serializers.CharField()
    uploaded_by = serializers.IntegerField()

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()
        return instance
