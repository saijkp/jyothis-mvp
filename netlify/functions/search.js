const axios = require('axios');

exports.handler = async (event) => {
    const keyword = event.queryStringParameters.q || 'acoustic panel';
    
    const options = {
        method: 'GET',
        url: 'https://otapi-1688.p.rapidapi.com/BatchSearchItemsFrame',
        params: { language: 'en', framePosition: '0', frameSize: '10', ItemTitle: keyword },
        headers: {
            'x-rapidapi-key': '94d703de80msh2eb28d6ac171df9p1e7d96jsn48a6076fe119',
            'x-rapidapi-host': 'otapi-1688.p.rapidapi.com'
        }
    };

    try {
        const response = await axios.request(options);
        const data = response.data;
        
        // Dig into the Otapi structure
        const items = data.Result?.Items?.Items?.Content || [];
        
        const results = items.slice(0, 3).map(item => {
            const price = item.Price?.OriginalPrice || item.Price?.Value || 0;
            return {
                title: item.Title,
                price_cny: price,
                img: item.MainPictureUrl,
                landed_gbp: Math.round((price * 0.11 * 1.55) * 1.08 * 100) / 100
            };
        });

        return {
            statusCode: 200,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
            body: JSON.stringify(results)
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
