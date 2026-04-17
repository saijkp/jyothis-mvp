import requests
import json

def handler(event, context):
    # Check if this is just a health check call
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}}

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
        
        # Exact path navigation for Otapi Batch
        items_list = data.get('Result', {}).get('Items', {}).get('Items', {}).get('Content', [])
        
        results = []
        for item in items_list[:3]:
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
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(results)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
