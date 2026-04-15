const axios = require('axios');

exports.handler = async (event) => {
    const { burden } = JSON.parse(event.body);
    const API_KEY = process.env.OPENAI_API_KEY;

    const prompt = `You are a Cyber-Taoist Master. A user is sacrificing a burden to the fire. 
    The burden is: "${burden}". 
    Respond in 2 sentences. Use the wisdom of the Tao Te Ching and Alan Watts. 
    Make it feel divine, mysterious, and deeply peaceful. Address the user's specific pain, but dissolve it into the infinite. Do not use corporate language.`;

    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: "gpt-4o",
            messages: [{ role: "system", content: prompt }]
        }, {
            headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' }
        });

        return {
            statusCode: 200,
            body: JSON.stringify({ reply: response.data.choices[0].message.content })
        };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
    }
};
