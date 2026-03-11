from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
# Create your models here.


User = get_user_model()

class CATEGORY:
    city_team = 'city_team'
    department = 'department'
    voltra_team = 'voltra_team'
    alumni = 'alumni'
    choices = [
        (alumni, 'Alumni'),
        (voltra_team, 'Voltra team'),
        (city_team,'City team'),
        (department,'Department'),
    ]

class EVENT_TYPE:
    online = 'online'
    offline = 'offline'

    choices = [
        (online, 'Online'),
        (offline, 'Offline'),
        
    ]

class EVENT_STATUS:
    approved = 'approved'
    rejected = 'rejected'
    new = 'new'
    reviewing = 'reviewing'
    

    choices = [
        (approved, 'Approved'),
        (rejected, 'Rejected'),
        (new,'New'),
        (reviewing,'Reviewing'),
    
        
    ]



class EventRequest(models.Model):
    eventrequest_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20,choices=CATEGORY.choices)
    event_type = models.CharField(max_length=50,choices=EVENT_TYPE.choices)
    objective = models.TextField()
    target_audience = models.CharField(max_length=200)
    expected_attendees = models.IntegerField()
    event_date = models.DateTimeField()
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices = EVENT_STATUS.choices,default=EVENT_STATUS.new)
    venue = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    speaker = models.ManyToManyField('event.Speaker',related_name='request_speakers')
    event_design = CloudinaryField('image')
    
    
    