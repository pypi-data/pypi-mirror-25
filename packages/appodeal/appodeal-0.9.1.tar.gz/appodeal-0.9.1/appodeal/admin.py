from django.contrib import admin

from appodeal import models


class RewardAdmin(admin.ModelAdmin):

    list_display = ('user_id', 'result', 'created_at')
    date_hierarchy = ('created_at')
    readonly_fields = ('data1', 'data2', 'output', 'user_id', 'amount', 'currency', 'impression_id', 'timestamp', 'hash', 'result')


admin.site.register(models.Reward, RewardAdmin)
