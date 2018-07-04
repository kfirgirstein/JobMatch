from django.contrib import admin
from app.models import *


admin.site.register(Company)
admin.site.register(Question)
admin.site.register(Status)
admin.site.register(Clusters)
admin.site.register(Questions_weights)
admin.site.register(Submissions)


