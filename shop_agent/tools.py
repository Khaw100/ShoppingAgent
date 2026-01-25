from util.mongodb import get_query_results, get_item_by_product_id, get_item_by_product_by_brand, get_item_by_material
from google.adk.tools import function_tool

@function_tool
def search_items(search_query: str):
    """Search items from vector DB by text query
    
    Args:
        search_query (str): text query for RAG
    Returns:
        context (str): Returned context from Retriever
    """
    if not search_query or not search_query.strip():
        raise RuntimeError("search_query is empty")
    try:
        results = get_query_results(search_query)

        if not results:
            return []
        return results
    except Exception as e:
        raise RuntimeError(f"search_items failed: {str(e)}")
@function_tool
def search_item_by_id(product_id: str):
    """Get item from DB by product_id 
    
    Args:
        product_id (str): id of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    if not product_id or not product_id.strip():
        raise RuntimeError("product_id is empty")
    
    try:
        results =  get_item_by_product_id(product_id)
        if not results:
                return []
        return results
    
    except Exception as e:
        raise RuntimeError(f"search_items failed: {str(e)}")
    
@function_tool      
def search_item_by_brand(brand: str):
    """Get item from DB by brand 
    
    Args:
        brand (str): brand of product 
    Returns:
        context (str): Returned context from DB 
    """ 
    if not brand or not brand.strip():
        raise RuntimeError("brand is empty")
    
    try:
        results = get_item_by_product_by_brand(brand)

        if not results:
            return []

        return results
    
    except Exception as e:
        raise RuntimeError(f"search_items failed: {str(e)}") 

@function_tool
def search_item_by_material(material: str):
    if not material or not material.strip():
        raise RuntimeError("material is empty")

    try:
        results = get_item_by_material(material)

        if not results:
            return []

        return results

    except Exception as e:
        raise RuntimeError(f"search_item_by_material failed: {str(e)}")