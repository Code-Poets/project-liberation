import assertpy
import pytest

from company_website.templatetags.variable_tag import define_variable


class TestDefineVariableTemplateTag:
    @pytest.mark.parametrize("value", ["Testowy tekst", 17, 15.5])
    def test_template_tag_should_return_variable_with_the_same_value(self, value):  # pylint: disable=no-self-use
        assertpy.assert_that(define_variable(value)).is_equal_to(value)
