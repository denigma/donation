from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
import itertools

currencies = (
    ('EUR', _l('Euro')),
    ('GBP', _l('British Pound')),
    ('USD', _l('USA Dollar')),
    ('BGL', _l('Bulgarian Lev')),
    ('HUF', _l('Hungarian Forint')),
)

anonimity = (
    (0, _l("Show name and donation")),
    (1, _l("Show name only")),
    (2, _l("Don't show donor details")),
)

class DonationsManager(models.Manager):
    def get_total(self, field='amount'):
        """Return the sum of the queryset's fields by amount."""
        return sum(super(DonationsManager, self).get_query_set().values_list(field, flat=True))

    def public(self):
        """Return only publicly shown donations."""
        return super(DonationsManager, self).get_query_set().filter(anoimity__lt=2)


class Donation(models.Model):
    txn = models.CharField(max_length=32, primary_key=True, help_text=_l("Transaction ID"))
    donor = models.CharField(max_length=255, blank=True, help_text=_l("The donor's name"))
    amount = models.IntegerField(help_text=_l("The amount donated"))
    currency = models.CharField(max_length=3, help_text=_l("The currency of the donation"))
    anonimity = models.IntegerField(choices=anonimity, default=0, help_text=_l("Show donor's name online"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = DonationsManager()

    class Meta:
        get_latest_by = 'created'
        verbose_name = _l('donation')
        verbose_name_plural = _l('donations')
        ordering = ['anonimity', '-amount', 'donor']

    def __unicode__(self):
        return '%s (%d %s)' % (self.donor, self.amount, self.currency)

    def save(self, force_insert=False, force_update=False):
        super(Donation, self).save(force_insert, force_update)

    def is_public_amount(self):
        if self.anonimity == 0:
            return True
        return False

    def is_public(self):
        if self.anonimity < 2:
            return True
        return False