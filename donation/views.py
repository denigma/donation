from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.contrib.sites.models import Site
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from donation import models, forms


class DonationView(TemplateView):
    template_name = 'donation/index.html'

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current
        context['total'] = models.Donation.objects.get_total
        context['donation_name'] =  settings.DONATION_NAME
        context['donation_number'] = settings.DONATION_NUMBER
        context['paypal_id'] = settings.PAYPAL_ID
        context['debug'] = settings.DEBUG
        return context


@csrf_exempt
def after_donation(request, template='donation/success.html'):
    """Process user actions as PayPal return the user"""
    # By default we return no form
    form = None
    if request.REQUEST.has_key('txn_id'):
        # Save the data we get from PayPal as anonymous
        data = {'txn': request.REQUEST['txn_id'],
                'amount': int(request.REQUEST['mc_gross'].split('.')[0]),
                'donor': '%s %s' % (request.REQUEST['first_name'],
                                    request.REQUEST['last_name']),
                'currency': request.REQUEST['mc_currency'][:3],
                'anonimity': 0,
                }
        inform = forms.DonationForm(data, initial=data)
        print inform
        if inform.is_valid():
            donation = inform.save()
            # Let the user modified her/his data
            form = forms.DonationForm(instance=donation)

    elif request.method=='POST':
        # If the user modified it
        try:
            instance = models.Donation.objects.get(pk=request.POST['txn'])
        except models.Donation.DoesNotExist:
            form = None
        else:
            form = forms.DonationForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
            return render_to_response(template, {'form': None}, RequestContext(request))
    return render_to_response(template, {'form': form}, RequestContext(request))