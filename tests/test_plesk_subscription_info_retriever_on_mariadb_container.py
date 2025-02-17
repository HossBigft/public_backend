import pytest
from app.ssh_plesk_subscription_info_retriever import query_subscription_info_by_domain
from tests.utils.container_db_utils import TestMariadb, TEST_DB_CMD
from tests.test_data.hosts import HostList
from unittest.mock import patch


@pytest.fixture(scope="module")
def init_test_db():
    testdb = TestMariadb().populate_db()

    def mock_batch_ssh(command: str):
        stdout = testdb.run_cmd(command)
        return [{"host": "test", "stdout": stdout}]

    with patch(
        "app.ssh_plesk_subscription_info_retriever.PLESK_DB_RUN_CMD", TEST_DB_CMD
    ):
        with patch(
            "app.ssh_plesk_subscription_info_retriever.batch_ssh_execute",
            wraps=mock_batch_ssh,
        ):
            yield testdb  # Yield the test database for use in tests


@pytest.mark.asyncio
async def test_get_existing_subscription_info(init_test_db):
    result = await query_subscription_info_by_domain(HostList.CORRECT_EXISTING_DOMAIN)

    expected_output = [
        {
            "host": "test",
            "id": "1184",
            "name": "gruzo.kz",
            "username": "FIO",
            "userlogin": "p-2342343",
            "domains": [
                "gruzo.kz",
                "sdfsd.gruzo.kz",
                "pomogite.gruzo.kz",
                "nodejs.gruzo.kz",
                "virtualizor.gruzo.kz",
                "wp.gruzo.kz",
                "onebula.gruzo.kz",
                "mxtest.gruzo.kz",
                "zone.gruzo.kz",
                "zless.gruzo.kz",
            ],
        }
    ]

    assert result == expected_output


@pytest.mark.asyncio
async def test_get_nonexisting_subscription_info(init_test_db):
    result = await query_subscription_info_by_domain("zless.kz")
    assert result is None
