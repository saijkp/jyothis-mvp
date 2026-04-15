exports.handler = async (event) => {
    if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method Not Allowed" };

    try {
        const { burden } = JSON.parse(event.body);
        const API_KEY = process.env.OPENAI_API_KEY;

        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: "gpt-4o",
                messages: [
                    { 
                        role: "system", 
                        content: "You are a Cyber-Taoist Master. Analyze the user's burden. Respond with a JSON object containing: 1. 'reply' (2 poetic sentences of wisdom) and 2. 'sigil' (A 2-3 word power-phrase in all caps that summarizes the transformation). Example: { 'reply': '...', 'sigil': 'UNBOUND WATER' }" 
                    },
                    { role: "user", content: `Sacrifice: ${burden}` }
                ],
                response_format: { type: "json_object" }
            })
        });

        const data = await response.json();
        return {
            statusCode: 200,
            body: data.choices[0].message.content // This sends the JSON back
        };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
    }
};
