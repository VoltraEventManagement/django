from django.db import models
from user.models import User
from event_request.models import EVENT_TYPE,CATEGORY
from cloudinary.models import CloudinaryField
# Create your models here.



class Speaker(models.Model):
    speaker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    
    


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=200)
    date = models.DateTimeField(null=False)
    city = models.TextField(max_length=100)
    description = models.TextField()
    event_speakers = models.ManyToManyField(Speaker,related_name='event_speakers')
    type = models.CharField(max_length=50,choices=EVENT_TYPE.choices)
    category = models.CharField(max_length=20,choices=CATEGORY.choices)
    target_audience = models.CharField(max_length=200)
    venue = models.BooleanField()
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)


class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    photo = CloudinaryField('image')
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE)



class EventUser(models.Model):
    eventuser_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    track = models.CharField(max_length=150)
    is_checked = models.BooleanField(default=False)
    

    class Meta:
        unique_together = ('event_id', 'user_id')


