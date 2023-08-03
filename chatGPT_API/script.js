import { config } from "dotenv"
import { Configuration, OpenAIApi } from "openai"

config()
const openai = new OpenAIApi(new Configuration({
    apiKey:process.env.API_KEY
}))

openai.createChatCompletion({
    model:"gpt-3.5-turbo",
    messages: [{role:"user", content: "Hello ChatGPT"}],
})
.then(res =>{
    console.log(res.data.choices[0])
})

// openai.createFineTune({
//     training_file: "C:\Users\Iris Nguyen\Documents\ChatGPT\Data\ML_output_scrambled.csv",
//   });