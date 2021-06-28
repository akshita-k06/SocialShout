from django.contrib import admin
from .models import complaint_category, complaint_subcategory, complaint_user
# Register your models here.
class complaint_subcategoryAdmin(admin.StackedInline):
    model=complaint_subcategory

@admin.register(complaint_category)
class complaint_categoryAdmin(admin.ModelAdmin):
    inlines=[complaint_subcategoryAdmin]
    list_display=("id","category")
    class Meta:
        model=complaint_category


@admin.register(complaint_subcategory)
class complaint_subcategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(complaint_user)
class complaint_userAdmin(admin.ModelAdmin):
    pass