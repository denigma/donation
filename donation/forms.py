from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from donation import models


class NoInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(value)

class NoHiddenInput(forms.Widget):
    is_hidden = True

    def render(self, name, value, attrs=None):
        return u''

class StaticField(forms.Field):
    widget = NoInput
    hidden_widget = NoHiddenInput

    def clean(self, value):
        return

class DonationForm(forms.ModelForm):
    txn = forms.CharField(label=_('Transaction ID'), widget=forms.HiddenInput, show_hidden_initial=True)
    donor = forms.CharField(label=_('Your name'))
    amount = StaticField(label=_('The amount donated'))
    currency = StaticField(label=_('The currency you have used'))
    anonimity = forms.ChoiceField(label=_('What anonimity do you prefer?'),
                                  choices=models.anonimity)

    class Meta:
        model = models.Donation

    def clean(self):
        for name, field in self.fields.items():
            if isinstance(field, StaticField):
                self.cleaned_data.update({name:self.initial[name]})

        return self.cleaned_data

    def save(self, commit=True):
        try:
            self.instance = models.Donation.objects.get(pk=self.cleaned_data['txn'])
        except models.Donation.DoesNotExist:
            pass
        return super(DonationForm, self).save(commit)