from util.mongodb import get_query_results, get_item_by_product_id, get_item_by_product_by_brand

def search_items(search_query: str):
    """Search items from vector DB by text query
    
    Args:
        search_query (str): text query for RAG
    Returns:
        context (str): Returned context from Retriever
    """
    try:
        return get_query_results(search_query)
    except Exception as e:
        return f"There was a problem while returning the tool: {str(e)}"
    
def get_item_by_id(product_id: str):
    """Get item from DB by product_id 
    
    Args:
        product_id (str): id of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    try:
        return get_item_by_product_id(product_id)
    except Exception as e:
        return f"There was a problem while returning the tool: {str(e)}" 
        
def search_item_by_brand(brand: str):
    """Get item from DB by brand 
    
    Args:
        brand (str): brand of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    try:
        return get_item_by_product_by_brand(brand)
    except Exception as e:
        return f"There was a problem while returning the tool: {str(e)}" 
        