import requests
import json

def handler(event, context):
    # Get the keyword from the URL (e.g., ?q=walnut+panel)
    keyword = event['queryStringParameters'].get('q', 'acoustic panel')
    
    url = "https://otapi-1688.p.rapidapi.com/BatchSearchItemsFrame"
    headers = {
        "x-rapidapi-key": "94d703de80msh2eb28d6ac171df9p1e7d96jsn48a6076fe119",
        "x-rapidapi-host": "otapi-1688.p.rapidapi.com"
    }
    params = {"language":"en","framePosition":"0","frameSize":"10", "ItemTitle": keyword}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Navigating the path we found in Colab
    content = data.get('Result', {}).get('Items', {}).get('Items', {}).get('Content', [])
    
    results = []
    for item in content[:3]: # Send top 3 back to the website
        price = item.get('Price', {}).get('OriginalPrice', 0)
        results.append({
            "title": item.get('Title'),
            "price_cny": price,
            "img": item.get('MainPictureUrl'),
            "landed_gbp": round((price * 0.11 * 1.55) * 1.08, 2)
        })

    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": json.dumps(results)
    }
