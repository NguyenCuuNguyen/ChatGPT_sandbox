const API_KEY = "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"

async function fetchData(){
    const  res = await fetch("https://api.openai.com/v1/chat/completions", {
        method : "POST",
        headers: {
            Authorization: `Bearer ${API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            prompt: "why use GPU?",
            max_tokens: 7
        })
    })
    const data = await res.json()
    console.log(data)
}

fetchData()