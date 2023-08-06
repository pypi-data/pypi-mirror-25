import pytest

import mongoengine


@pytest.fixture()
def initialize_separate_test_db():
    mongoengine.connect("testpyishdb")
