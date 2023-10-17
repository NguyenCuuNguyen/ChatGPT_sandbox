import { config } from "dotenv"
import { Configuration, OpenAIApi } from "openai"
import readline from "readline"
config()
const openai = new OpenAIApi(new Configuration({
    apiKey:process.env.API_KEY
}))

const userInterface = readline.createInterface({
    input: process.stdin,
    output: process.stdout
})

//get user's input
userInterface.prompt()
//loop
userInterface.on("line", async input => {
    //send user input to chatGPT
    const res = await openai.createChatCompletion({
        model:"gpt-3.5-turbo",
        messages: [{role:"user", content: input}],
    })
    console.log(res.data.choices[0].message.content)
    userInterface.prompt()
    // .then(res =>{
    //     console.log(res.data.choices[0])
    // })
})




// openai.createFineTune({
//     training_file: "C:\Users\Iris Nguyen\Documents\ChatGPT\Data\ML_output_scrambled.csv",
//   });