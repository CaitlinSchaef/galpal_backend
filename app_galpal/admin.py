from django.contrib import admin
from app_galpal.models import *


class ProfileAdmin(admin.ModelAdmin):
  pass

class MatchProfileAnswersAdmin(admin.ModelAdmin):
  pass

class MatchProfileDisplayAdmin(admin.ModelAdmin):
  pass

class InterestInventoryAdmin(admin.ModelAdmin):
  pass

class RequestedMatchAdmin(admin.ModelAdmin):
  pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(MatchProfileAnswers, MatchProfileAnswersAdmin)
admin.site.register(MatchProfileDisplay, MatchProfileDisplayAdmin)
admin.site.register(InterestInventory, InterestInventoryAdmin)
admin.site.register(RequestedMatch, RequestedMatchAdmin)
