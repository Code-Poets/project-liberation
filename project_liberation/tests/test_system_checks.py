from django.conf import settings
from django.test import TestCase
from django.test import override_settings

from project_liberation.system_check import GOOGLE_API_KEYS_ERRORS
from project_liberation.system_check import check_google_api_key


class TestGoogleApiKeyCheck(TestCase):
    @override_settings(GOOGLE_API_KEY="I-JuSTMade_y0u-Up_toHurtmYSelf_yesI-Did")
    def test_check_google_api_key_with_accurate_setting(self):
        errors = check_google_api_key(None)
        self.assertEqual(errors, [])

    @override_settings(GOOGLE_API_KEY="heADlIKeAHolE_BlAckaS_yoUrSOulIDratHeR_dIEthaNGiVEy0u_c0ntRoL")
    def test_check_google_api_key_with_too_long_setting(self):
        errors = check_google_api_key(None)
        self.assertEqual(errors[0], GOOGLE_API_KEYS_ERRORS["length"])

    @override_settings(GOOGLE_API_KEY="WIll_Y0ubIte-tHEhaNd_THaTfeEdsy0u")
    def test_check_google_api_key_with_too_short_setting(self):
        errors = check_google_api_key(None)
        self.assertEqual(errors[0], GOOGLE_API_KEYS_ERRORS["length"])

    @override_settings(GOOGLE_API_KEY=[])
    def test_check_google_api_key_with_wrong_type_setting(self):
        errors = check_google_api_key(None)
        self.assertEqual(errors[0], GOOGLE_API_KEYS_ERRORS["type"])

    @override_settings()
    def test_check_google_api_key_with_no_setting(self):
        del settings.GOOGLE_API_KEY
        errors = check_google_api_key(None)
        self.assertEqual(errors[0], GOOGLE_API_KEYS_ERRORS["empty"])
