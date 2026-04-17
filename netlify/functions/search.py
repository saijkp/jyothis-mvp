import requests
import json

def handler(event, context):
    # Get the keyword from the URL
    params_in = event.get('queryStringParameters', {})
    keyword = params_in.get('q', 'acoustic panel')
    
    url = "https://otapi-1688.p.rapidapi.com/BatchSearchItemsFrame"
    headers = {
        "x-rapidapi-key": "94d703de80msh2eb28d6ac171df9p1e7d96jsn48a6076fe119",
        "x-rapidapi-host": "otapi-1688.p.rapidapi.com"
    }
    params = {"language":"en","framePosition":"0","frameSize":"10", "ItemTitle": keyword}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        # Navigation path for Otapi BatchSearchItemsFrame
        result_layer = data.get('Result', {})
        items_outer = result_layer.get('Items', {})
        items_inner = items_outer.get('Items', {})
        content = items_inner.get('Content', [])
        
        results = []
        for item in content[:3]:
            price_info = item.get('Price', {})
            price = price_info.get('OriginalPrice', price_info.get('Value', 0))
            results.append({
                "title": item.get('Title'),
                "price_cny": price,
                "img": item.get('MainPictureUrl'),
                "landed_gbp": round((price * 0.11 * 1.55) * 1.08, 2)
            })

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(results)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
