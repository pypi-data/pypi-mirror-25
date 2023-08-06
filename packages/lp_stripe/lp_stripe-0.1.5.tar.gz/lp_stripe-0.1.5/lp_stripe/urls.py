from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SubscriptionCreateView, SubscriptionRetrieveView

urlpatterns = {
    url(r'^stripe/subscription', SubscriptionCreateView.as_view(), name='lp_stripe_subscriptioncreate'),
    url(r'^account/subscription', SubscriptionRetrieveView.as_view(), name='lp_stripe_subscriptionretrieve')
}

urlpatterns = format_suffix_patterns(urlpatterns)
