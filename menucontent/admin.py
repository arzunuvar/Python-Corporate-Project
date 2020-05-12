from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from menucontent.models import MImages, Menu, Menucontent


class MenucontentImageInline(admin.TabularInline):
    model = MImages
    extra = 3


class MenucontentInline(admin.TabularInline):
    model = Menucontent
    extra = 1


class MenucontentAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'image_tag', 'status', 'create_at']
    list_filter = ['status', 'type']
    inlines = [MenucontentImageInline]
    prepopulated_fields = {'slug': ('title',)}


class MenuAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ['tree_actions', 'indented_title', 'status']
    list_filter = ['status']
    inlines = [MenucontentInline]


admin.site.register(Menu, MenuAdmin)
admin.site.register(Menucontent, MenucontentAdmin)
