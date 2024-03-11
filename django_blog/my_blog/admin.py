from django.contrib import admin
from my_blog.models import ImageUpload, Category, Product, UserDetailModel, FavouriteModel

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id","category","name","thumbnail","user")
    list_filter = ("category","user","created_at")
    search_fields = ("name",)


admin.site.register(ImageUpload)
admin.site.register(Category)
admin.site.register(Product,PostAdmin)
admin.site.register(UserDetailModel)
admin.site.register(FavouriteModel)



