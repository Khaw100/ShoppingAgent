from util.mongodb import get_query_results, get_item_by_product_id, get_item_by_product_by_brand, get_item_by_material, create_transaction, get_user_transactions
# from google.adk.runtime import get_current_context

def search_items(search_query: str):
    """Search items from vector DB by text query
    
    Args:
        search_query (str): text query for RAG
    Returns:
        context (str): Returned context from Retriever
    """
    try:
        results = get_query_results(search_query)
        return {"results": results}
    except Exception as e:
        return {"error" : f"There was a problem while returning the tool: {str(e)}"}
    
def search_item_by_id(product_id: str):
    """Get item from DB by product_id 
    
    Args:
        product_id (str): id of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    try:
        results = get_item_by_product_id(product_id)
        return {"results": results}
    except Exception as e:
        return {"error":f"There was a problem while returning the tool: {str(e)}"}
        
def search_item_by_brand(brand: str):
    """Get item from DB by brand 
    
    Args:
        brand (str): brand of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    try:
        results = get_item_by_product_by_brand(brand)
        return {"results": results}
    except Exception as e:
        return {"error":f"There was a problem while returning the tool: {str(e)}"} 

def search_item_by_material(material: str):
    if not material or not material.strip():
        raise RuntimeError("material is empty")

    try:
        results = get_item_by_material(material)

        if not results:
            return []

        return {"results": results}

    except Exception as e:
        return {"error":f"search_item_by_material failed: {str(e)}"}
    

def buy_item(product_id: str):
    try:
        # ctx = get_current_context()
        user_id = "user"
        items = get_item_by_product_id(product_id)

        if not items:
            return {"error": "Product not found"}

        product = items[0]

        trx = create_transaction(
            user_id=user_id,
            product={
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"]
            }
        )

        return {
            "final": True,
            "text": f"Purchase successful!\n\n"
                    f"Item: {trx['product_name']}\n"
                    f"Price: ${trx['price']} {trx['currency']}\n"
                    f"Order time: {trx['created_at']}"
        }

    except Exception as e:
        return {"error": str(e)}

def get_my_transactions():
    user_id = "user"
    trxs = get_user_transactions(user_id)

    if not trxs:
        return {
            "final": True,
            "text": "🛒 You have no transactions yet."
        }

    lines = []
    for trx in trxs:
        lines.append(
            f"- {trx['product_name']} | "
            f"${trx['price']} {trx['currency']} | "
            f"{trx['created_at']}"
        )

    return {
        "final": True,
        "text": "📜 Your transaction history:\n" + "\n".join(lines)
    }