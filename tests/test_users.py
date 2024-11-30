from .conftest import *


@pytest.mark.django_db
class TestUsersModels(BaseTest):
    """
    users models
    - model field validations
    """

    def test_profile(self):
        assert self.user.email
        assert self.user.password
