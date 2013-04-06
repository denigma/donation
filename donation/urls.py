from django.conf.urls import patterns, url

from donation.views import DonationView


urlpatterns = patterns('donation.views',
    url(r'^$', DonationView.as_view(), name='donation-index'),
    url(r'^success/$', 'after_donation', name='donation-success'),
)