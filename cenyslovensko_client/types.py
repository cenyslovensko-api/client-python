from __future__ import annotations

from typing import TypedDict


class VersionResponse(TypedDict):
    version: str


class Vendor(TypedDict):
    id: str
    name: str


class VendorsResponse(TypedDict):
    vendors: list[Vendor]


class ProductPriceBranch(TypedDict):
    branchId: str
    price: float
    unitPrice: float


class ProductPriceItem(TypedDict):
    productKey: str
    ean: str
    internalId: str
    companyId: str
    reportDate: str
    prices: list[ProductPriceBranch]


class ProductPricesPage(TypedDict):
    page: int
    size: int
    count: int
    content: list[ProductPriceItem]


class ProductPricesCurrentDayResponse(TypedDict):
    product_prices: ProductPricesPage


class ProductResponse(TypedDict, total=False):
    id: str
    name: str
    sku: str
