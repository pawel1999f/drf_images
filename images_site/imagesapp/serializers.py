from django.contrib.auth.models import User
from rest_framework import serializers

from imagesapp.models import Profile, ImageModel, LinkModel

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='creator.id')
    
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=ImageModel.objects.all())
    
    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'account_tier', 'images']
        lookup_field = 'user_id'
        extra_kwargs = {
            'url': {'lookup_field': 'user_id'}
        }
        
class ImageModelSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source='creator.username')
    creator_id = serializers.ReadOnlyField(source='creator.id')
    image_url = serializers.ImageField(required=False)
    
    links = serializers.SerializerMethodField()
    expiring_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageModel
        fields = ['id', 'creator', 'creator_id', 'image_url', 'expiring_url', 'links']
        
    def get_links(self, obj):
        request = self.context.get('request')
        link_dict = {}
        related_links = LinkModel.objects.all().filter(related_image_model = obj)
        for link in related_links:
            link_dict[link.height] = request.build_absolute_uri(link.url.url)
        return link_dict
    
    def get_expiring_url(self, obj):
        return "didnt quite get that one"