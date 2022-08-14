from django.db.models import Avg
from rest_framework import serializers

from applications.post.models import Image, Post, Comment
from applications.notifications.tasks import send_product_info


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    owner = serializers.ReadOnlyField(source='owner.email')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES

        post = Post.objects.create(**validated_data)
        for image in images.getlist('images'):
            Image.objects.create(product=post, image=image)

        send_product_info.delay(validated_data['owner'].email)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        # representation['comments'] = instance.comments.get_or_create()
        return representation


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
