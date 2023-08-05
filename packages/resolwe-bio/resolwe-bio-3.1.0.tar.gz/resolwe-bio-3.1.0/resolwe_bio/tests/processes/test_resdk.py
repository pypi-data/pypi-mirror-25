from django.contrib.auth.models import AnonymousUser
from django.test import LiveServerTestCase
from guardian.shortcuts import assign_perm
from resolwe_bio.utils.test import TransactionBioProcessTestCase
from resolwe.test.utils import with_resolwe_host

class LenDSSTestCase(TransactionBioProcessTestCase, LiveServerTestCase):
    @with_resolwe_host
    def test_dss_len(self):
        adapters = self.prepare_adapters()
        assign_perm('view_data', AnonymousUser(), adapters)
        self.run_process('dss-len-test', {
            'adapters': adapters.id,
        })
