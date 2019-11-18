from django.conf import settings
from django.test import TestCase
from django.test import override_settings

from project_liberation.system_check import GOOGLE_API_KEYS_ERRORS
from project_liberation.system_check import check_custom_storage_directories
from project_liberation.system_check import check_google_api_key
from project_liberation.system_check import setting_not_a_string_error
from project_liberation.system_check import setting_not_declared_error


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


class TestStorageDirectoriesCheck(TestCase):
    @override_settings()
    def test_check_company_employees_storage_with_no_setting(self):
        del settings.COMPANY_EMPLOYEES_STORAGE
        errors = check_custom_storage_directories(None)
        self.assertTrue(setting_not_declared_error("COMPANY_EMPLOYEES_STORAGE") in errors)

    @override_settings(COMPANY_EMPLOYEES_STORAGE=123)
    def test_check_company_employees_storage_with_wrong_type_setting(self):
        errors = check_custom_storage_directories(None)
        self.assertTrue(setting_not_a_string_error("COMPANY_EMPLOYEES_STORAGE") in errors)

    @override_settings(COMPANY_EMPLOYEES_STORAGE="company_employees_storage")
    def test_check_company_employees_storage_with_accurate_setting(self):
        errors = check_custom_storage_directories(None)
        self.assertEqual(errors, [])

    @override_settings()
    def test_check_testimonial_photos_storage_with_no_setting(self):
        del settings.TESTIMONIAL_PHOTOS_STORAGE
        errors = check_custom_storage_directories(None)
        self.assertTrue(setting_not_declared_error("TESTIMONIAL_PHOTOS_STORAGE") in errors)

    @override_settings(TESTIMONIAL_PHOTOS_STORAGE=123)
    def test_check_testimonial_photos_storage_with_wrong_type_setting(self):
        errors = check_custom_storage_directories(None)
        self.assertTrue(setting_not_a_string_error("TESTIMONIAL_PHOTOS_STORAGE") in errors)

    @override_settings(TESTIMONIAL_PHOTOS_STORAGE="testimonial_photos_storage")
    def test_check_testimonial_photos_storage_with_accurate_setting(self):
        errors = check_custom_storage_directories(None)
        self.assertEqual(errors, [])
