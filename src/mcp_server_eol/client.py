"""
Client for the endoflife.date API with Pydantic models.
"""

import asyncio
import logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
import httpx
from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class CycleInfo(BaseModel):
    """Information about a specific product cycle/version."""
    cycle: str = Field(..., description="Version/cycle identifier")
    release_date: Optional[Union[str, date]] = Field(None, alias="releaseDate", description="Release date")
    eol: Optional[Union[str, date, bool]] = Field(None, description="End of life date or status")
    latest: Optional[str] = Field(None, description="Latest patch version")
    latest_release_date: Optional[Union[str, date]] = Field(None, alias="latestReleaseDate", description="Latest release date")
    lts: Optional[Union[bool, str, date]] = Field(None, description="Long term support status or date")
    support: Optional[Union[str, date, bool]] = Field(None, description="Support end date or status")
    
    class Config:
        populate_by_name = True


class ProductInfo(BaseModel):
    """Information about a product and its versions."""
    product: str = Field(..., description="Product name")
    versions: List[CycleInfo] = Field(..., description="List of product versions/cycles")
    count: int = Field(..., description="Number of versions")


class SearchResult(BaseModel):
    """Search results for products."""
    results: List[str] = Field(..., description="List of matching product names")
    count: int = Field(..., description="Number of results found")
    query: str = Field(..., description="Original search query")


class AllProductsResult(BaseModel):
    """Result containing all tracked products."""
    products: List[str] = Field(..., description="List of all product names")
    count: int = Field(..., description="Total number of products")


class SupportStatus(BaseModel):
    """Support status information for a specific version."""
    product: str = Field(..., description="Product name")
    version: str = Field(..., description="Version identifier")
    found: bool = Field(..., description="Whether the version was found")
    cycle_info: Optional[CycleInfo] = Field(None, description="Detailed cycle information")
    is_supported: bool = Field(..., description="Whether version is actively supported")
    is_eol: bool = Field(..., description="Whether version has reached end of life")


class CycleDetails(BaseModel):
    """Detailed information about a specific cycle."""
    product: str = Field(..., description="Product name")
    cycle: str = Field(..., description="Cycle identifier")
    details: CycleInfo = Field(..., description="Detailed cycle information")


class EndOfLifeClient:
    """Client for interacting with the endoflife.date API."""

    def __init__(self, base_url: str = "https://endoflife.date/api"):
        self.base_url = base_url
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_all_products(self) -> AllProductsResult:
        """Get a list of all products tracked by endoflife.date."""
        try:
            response = await self._client.get(f"{self.base_url}/all.json")
            response.raise_for_status()
            products = response.json()
            
            return AllProductsResult(
                products=products,
                count=len(products)
            )
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            raise

    async def search_products(self, query: str) -> SearchResult:
        """Search for products by name (case-insensitive partial match)."""
        try:
            all_products = await self.get_all_products()
            query_lower = query.lower()
            
            matching_products = [
                product for product in all_products.products
                if query_lower in product.lower()
            ]
            
            return SearchResult(
                results=matching_products,
                count=len(matching_products),
                query=query
            )
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise

    async def get_product_versions(self, product: str) -> ProductInfo:
        """Get all versions/cycles for a specific product."""
        try:
            response = await self._client.get(f"{self.base_url}/{product}.json")
            response.raise_for_status()
            versions_data = response.json()
            
            # Convert raw data to CycleInfo models
            cycles = []
            for version_data in versions_data:
                cycle_info = CycleInfo(**version_data)
                cycles.append(cycle_info)
            
            return ProductInfo(
                product=product,
                versions=cycles,
                count=len(cycles)
            )
        except Exception as e:
            logger.error(f"Error getting product versions for {product}: {e}")
            raise

    async def get_cycle_details(self, product: str, cycle: str) -> CycleDetails:
        """Get detailed information about a specific product cycle."""
        try:
            response = await self._client.get(f"{self.base_url}/{product}/{cycle}.json")
            response.raise_for_status()
            cycle_data = response.json()
            
            cycle_info = CycleInfo(cycle=cycle, **cycle_data)
            
            return CycleDetails(
                product=product,
                cycle=cycle,
                details=cycle_info
            )
        except Exception as e:
            logger.error(f"Error getting cycle details for {product} {cycle}: {e}")
            raise

    async def check_support_status(self, product: str, version: str) -> SupportStatus:
        """Check if a specific product version is still supported."""
        try:
            # First, try to get the specific cycle
            try:
                cycle_details = await self.get_cycle_details(product, version)
                return SupportStatus(
                    product=product,
                    version=version,
                    found=True,
                    cycle_info=cycle_details.details,
                    is_supported=self._is_version_supported(cycle_details.details),
                    is_eol=self._is_version_eol(cycle_details.details)
                )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    # If specific version not found, search through all versions
                    product_info = await self.get_product_versions(product)
                    for cycle in product_info.versions:
                        if (cycle.cycle == version or 
                            cycle.latest == version or
                            str(cycle.cycle).startswith(version)):
                            return SupportStatus(
                                product=product,
                                version=version,
                                found=True,
                                cycle_info=cycle,
                                is_supported=self._is_version_supported(cycle),
                                is_eol=self._is_version_eol(cycle)
                            )
                    
                    # Version not found
                    return SupportStatus(
                        product=product,
                        version=version,
                        found=False,
                        cycle_info=None,
                        is_supported=False,
                        is_eol=True
                    )
                else:
                    raise
        except Exception as e:
            logger.error(f"Error checking support status for {product} {version}: {e}")
            raise

    def _is_version_supported(self, cycle_info: CycleInfo) -> bool:
        """Check if a version is currently supported based on cycle info."""
        # Check support date
        support_date = cycle_info.support
        if support_date is not None:
            if isinstance(support_date, bool):
                return support_date
            elif isinstance(support_date, (str, date)):
                try:
                    if isinstance(support_date, str):
                        support_end = datetime.fromisoformat(support_date.replace('Z', '+00:00')).date()
                    else:
                        support_end = support_date
                    return date.today() <= support_end
                except (ValueError, TypeError):
                    pass

        # Check EOL date as fallback
        eol_date = cycle_info.eol
        if eol_date is not None:
            if isinstance(eol_date, bool):
                return not eol_date
            elif isinstance(eol_date, (str, date)):
                try:
                    if isinstance(eol_date, str):
                        eol_end = datetime.fromisoformat(eol_date.replace('Z', '+00:00')).date()
                    else:
                        eol_end = eol_date
                    return date.today() <= eol_end
                except (ValueError, TypeError):
                    pass

        return False

    def _is_version_eol(self, cycle_info: CycleInfo) -> bool:
        """Check if a version has reached end of life."""
        eol_date = cycle_info.eol
        if eol_date is None:
            return False
        
        if isinstance(eol_date, bool):
            return eol_date
        elif isinstance(eol_date, (str, date)):
            try:
                if isinstance(eol_date, str):
                    eol_end = datetime.fromisoformat(eol_date.replace('Z', '+00:00')).date()
                else:
                    eol_end = eol_date
                return date.today() > eol_end
            except (ValueError, TypeError):
                return False
        
        return False


# Export the models for use in other modules
__all__ = [
    'EndOfLifeClient',
    'CycleInfo', 
    'ProductInfo',
    'SearchResult',
    'AllProductsResult',
    'SupportStatus',
    'CycleDetails'
]
