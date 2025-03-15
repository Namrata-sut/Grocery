import pytest

from app.models.product_model import ProductModel


@pytest.mark.asyncio
async def test_get_product_by_id(async_client, async_db):
    # ✅ Insert test data
    new_product = ProductModel(name="Peanut Butter", price=100, stock=10000)
    async_db.add(new_product)
    await async_db.commit()
    await async_db.refresh(new_product)  # ✅ Ensure it has an ID

    # ✅ Send GET request
    response = await async_client.get(f"/get_product_by_id/{new_product.id}")

    # ✅ Assert correct response
    assert response.status_code == 200
    assert response.json() == {
        "id": new_product.id,
        "name": "Peanut Butter",
        "price": 100,
        "stock": 10000,
    }
