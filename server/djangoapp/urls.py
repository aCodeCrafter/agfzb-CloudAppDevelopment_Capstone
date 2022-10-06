from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route='dealership', view=views.render_generic_static_page, name='static_page'),
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about',view=views.about,name='About'),
    # path for contact us view
    path(route='contact',view=views.contact,name='Contact'),
    # path for registration
    path(route='register',view=views.registration_request,name='Logout'),
    # path for login
    path(route='login',view=views.login_request,name='Login'),
    # path for logout
    path(route='logout',view=views.logout_request,name='Logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='Dealer Reviews'),
    # path for add a review view
    path(route='dealer/<int:dealer_id>/submit_review', view=views.add_review, name='Submit Review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
