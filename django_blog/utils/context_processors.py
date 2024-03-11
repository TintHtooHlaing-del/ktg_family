from my_blog.models import Category, FavouriteModel

def category(request):
    category = Category.objects.all()
    return {'category':category}

def favouriteCount(request):
    count = FavouriteModel.objects.filter(user_id=request.user.id).count()
    return {'count':count}
