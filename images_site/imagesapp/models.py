from django.db import models
 
from django.contrib.auth.models import User

from imagesapp.utils import get_thumbnail_sizes 

import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models

MAX_INT = 2147483647

# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class ImageModel(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        pk_before = self.pk
            
        super().save(*args, **kwargs)
        
        if pk_before is None:
            self.upload_images()
        
            
    def upload_images(self, *args, **kwargs):
        creator_tier = self.creator.profile.account_tier
        heights = get_thumbnail_sizes(creator_tier.thumbnail_sizes)
        include_original_file = creator_tier.original_file
        include_generate_expiring = creator_tier.generate_expiring
        
        for height in heights:
            self.upload_resized_image(self.image_url, height)
        if include_original_file:
            self.upload_resized_image(self.image_url, None)
            
    def upload_resized_image(self, image_url, height = None):
        link = LinkModel(related_image_model=self, height=height, url=image_url)
        link.save()
        
    
class LinkModel(models.Model):
    related_image_model = models.ForeignKey(
        ImageModel, on_delete=models.CASCADE)#, related_name="listings")
    height = models.CharField(max_length=200, null=True)
    url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            h = self.height
            if h is None:
                self.height = "original"
                h = MAX_INT
            self.resize(self.url, (MAX_INT, h))

        super().save(*args, **kwargs)
        
    def resize(self, imageField: models.ImageField, size:tuple):
        im = Image.open(imageField)
        source_image = im.convert('RGB')
        source_image.thumbnail(size)
        output = BytesIO()
        source_image.save(output, format='JPEG')
        output.seek(0)

        content_file = ContentFile(output.read())
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.jpeg'
        imageField.save(random_name, file, save=False)

class AccountTier(models.Model):
    tier_name = models.CharField(max_length=200)
    thumbnail_sizes = models.CharField(max_length=200)
    original_file = models.BooleanField(default=False)
    generate_expiring = models.BooleanField(default=False)
    
    def __str__(self):
        return self.tier_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(
        AccountTier, on_delete=models.CASCADE)