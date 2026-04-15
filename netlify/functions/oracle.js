exports.handler = async (event) => {
    // Only allow POST requests
    if (event.httpMethod !== "POST") {
        return { statusCode: 405, body: "Method Not Allowed" };
    }

    try {
        const { burden } = JSON.parse(event.body);
        const API_KEY = process.env.OPENAI_API_KEY;

        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "gpt-4o",
                messages: [
                    { 
                        role: "system", 
                        content: "You are a Cyber-Taoist Master. The user is sacrificing a burden to the fire. Use the wisdom of the Tao Te Ching and Alan Watts. Respond in exactly 2 sentences. Be divine, direct, and poetic. Address their specific pain but dissolve it into the infinite." 
                    },
                    { 
                        role: "user", 
                        content: `I sacrifice this burden: ${burden}` 
                    }
                ]
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error ? data.error.message : 'OpenAI API Error');
        }

        return {
            statusCode: 200,
            body: JSON.stringify({ reply: data.choices[0].message.content })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
