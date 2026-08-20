from __future__ import annotations

import os
from typing import Any, Mapping, Sequence

from ..errors import RpcClientError
from ..ports import RpcTransport
from ..rpc_session import RpcSession
from ..types import ProductPricesCurrentDayResponse


class CenyslovenskoProductPricesRpcClient:
    def __init__(
        self,
        command: Sequence[str] | None = None,
        cwd: str | os.PathLike[str] | None = None,
        env: Mapping[str, str] | None = None,
        timeout_seconds: float = 15.0,
        transport: RpcTransport | None = None,
        session: RpcSession | None = None,
    ) -> None:
        self._session = session or RpcSession(
            command=command,
            cwd=cwd,
            env=env,
            timeout_seconds=timeout_seconds,
            transport=transport,
        )

    def __enter__(self) -> "CenyslovenskoProductPricesRpcClient":
        self.start()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def start(self) -> None:
        self._session.start()

    def close(self) -> None:
        self._session.close()

    def call(self, method: str, params: Any = None) -> Any:
        return self._session.call(method=method, params=params)

    def get_current_day_prices(
        self,
        branch_ids: Sequence[str] | None = None,
        order_by: str = "unit_price",
        sort_order: str = "asc",
        only_in_my_branches: bool = True,
        category_id: int | None = None,
        group_by_vendor: bool = False,
        page: int = 0,
        size: int = 25,
    ) -> ProductPricesCurrentDayResponse:
        params: dict[str, Any] = {
            "branchIds": list(branch_ids or []),
            "orderBy": order_by,
            "sortOrder": sort_order,
            "onlyInMyBranches": only_in_my_branches,
            "categoryId": category_id,
            "groupByVendor": group_by_vendor,
            "page": page,
            "size": size,
        }
        response: ProductPricesCurrentDayResponse = self.call("product-prices.current-day.get", params)
        if not isinstance(response, dict):
            raise RpcClientError("Missing or invalid product prices payload in response")
        return response
