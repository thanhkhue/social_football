from django.contrib import admin
from .models import Account, Field, Slot, Match, City, District, Photo, Comment

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['first_name', 'username', 'last_name', 'email']
    ordering = ['first_name']


    fieldsets = [
        ('Account Detail', {
            'fields': ['first_name', 'username', 'email',
                       'is_active', 'is_staff', 'is_superuser',
                       'gender', 'birthday', 'description',
                       'timezone', 'district_id', 'verification_code'],
        }),
    ]

    class Meta:
        model = Account


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price_morning',
                    'price_afternoon', 'price_evening',
                     'phone_number', 'rating', 'lng', 'lat')
    ordering = ['name']

    fieldsets = [
            ('Field Detail', {
                'fields': ['name', 'address', 'phone_number', 'rating',
                'price_morning', 'price_afternoon', 'price_evening',
                'lat', 'lng', 'district_id','size'],
            }),
        ]
    class Meta:
        model = Field

class SlotAdmin(admin.ModelAdmin):
    pass

class CityAdmin(admin.ModelAdmin):
    pass

class DistrictAdmin(admin.ModelAdmin):
    pass

class MatchAdmin(admin.ModelAdmin):
    pass

class PhotoAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'match_object', 'date_created', 'comment')


admin.site.register(Field, FieldAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
