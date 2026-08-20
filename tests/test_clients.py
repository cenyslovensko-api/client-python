from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cenyslovensko_client.clients.prices import CenyslovenskoProductPricesRpcClient
from cenyslovensko_client.clients.product import CenyslovenskoProductRpcClient
from cenyslovensko_client.clients.vendor import CenyslovenskoVendorRpcClient
from cenyslovensko_client.clients.version import CenyslovenskoVersionRpcClient
from cenyslovensko_client.errors import RpcClientError


class FakeSession:
    def __init__(self, responses: dict[str, object] | None = None) -> None:
        self.responses = responses or {}
        self.calls: list[tuple[str, object]] = []
        self.started = False
        self.closed = False

    def start(self) -> None:
        self.started = True

    def close(self) -> None:
        self.closed = True

    def call(self, method: str, params: object = None) -> object:
        self.calls.append((method, params))
        if method in self.responses:
            return self.responses[method]
        return {}


class ClientTests(unittest.TestCase):
    def test_version_client_reads_version(self) -> None:
        session = FakeSession({"version.get": {"version": "0.1.370"}})
        client = CenyslovenskoVersionRpcClient(session=session)

        version = client.get_version()

        self.assertEqual(version, "0.1.370")
        self.assertEqual(session.calls[0], ("version.get", None))

    def test_version_client_rejects_invalid_version_shape(self) -> None:
        session = FakeSession({"version.get": {"version": 123}})
        client = CenyslovenskoVersionRpcClient(session=session)

        with self.assertRaises(RpcClientError):
            client.get_version()

    def test_product_client_uses_product_method(self) -> None:
        session = FakeSession({"product.get": {"id": "123"}})
        client = CenyslovenskoProductRpcClient(session=session)

        result = client.get_product("123")

        self.assertEqual(result, {"id": "123"})
        self.assertEqual(session.calls[0], ("product.get", {"id": "123"}))

    def test_vendor_client_reads_vendors(self) -> None:
        vendors = [{"id": "abc", "name": "Vendor One"}]
        session = FakeSession({"vendor.get": {"vendors": vendors}})
        client = CenyslovenskoVendorRpcClient(session=session)

        result = client.get_vendors()

        self.assertEqual(result, vendors)
        self.assertEqual(session.calls[0], ("vendor.get", None))

    def test_product_prices_client_reads_current_day_prices(self) -> None:
        payload = {"product_prices": {"count": 1}}
        session = FakeSession({"product-prices.current-day.get": payload})
        client = CenyslovenskoProductPricesRpcClient(session=session)

        result = client.get_current_day_prices(branch_ids=["1061_50020188"], page=0, size=25)

        self.assertEqual(result, payload)
        self.assertEqual(
            session.calls[0],
            (
                "product-prices.current-day.get",
                {
                    "branchIds": ["1061_50020188"],
                    "orderBy": "unit_price",
                    "sortOrder": "asc",
                    "onlyInMyBranches": True,
                    "categoryId": None,
                    "groupByVendor": False,
                    "page": 0,
                    "size": 25,
                },
            ),
        )

    def test_context_manager_starts_and_closes(self) -> None:
        session = FakeSession({"version.get": {"version": "0.1.370"}})

        with CenyslovenskoVersionRpcClient(session=session) as client:
            _ = client.get_version()

        self.assertTrue(session.started)
        self.assertTrue(session.closed)


if __name__ == "__main__":
    unittest.main()
