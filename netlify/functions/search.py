import requests
import json

def handler(event, context):
    try:
        params_in = event.get('queryStringParameters', {})
        keyword = params_in.get('q', 'acoustic panel')
        
        url = "https://otapi-1688.p.rapidapi.com/BatchSearchItemsFrame"
        headers = {
            "x-rapidapi-key": "94d703de80msh2eb28d6ac171df9p1e7d96jsn48a6076fe119",
            "x-rapidapi-host": "otapi-1688.p.rapidapi.com"
        }
        params = {"language":"en","framePosition":"0","frameSize":"10", "ItemTitle": keyword}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            return {"statusCode": response.status_code, "body": json.dumps({"error": "RapidAPI Rejected Request"})}

        data = response.json()
        
        # Safe digging into Otapi structure
        items_list = data.get('Result', {}).get('Items', {}).get('Items', {}).get('Content', [])
        
        results = []
        for item in items_list[:3]:
            price_info = item.get('Price', {})
            price = price_info.get('OriginalPrice', price_info.get('Value', 0))
            results.append({
                "title": item.get('Title', 'Item'),
                "price_cny": price,
                "img": item.get('MainPictureUrl', ''),
                "landed_gbp": round((float(price) * 0.11 * 1.55) * 1.08, 2)
            })

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps(results)
        }

    except Exception as e:
        return {
            "statusCode": 500, 
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"debug_error": str(e)})
        }
