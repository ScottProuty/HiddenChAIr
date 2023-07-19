import os
import openai
import webbrowser

openai.api_key = os.getenv("OPENAI_API_KEY")

def SetupGame():
    points = 10
    frame = 1
    

def GenerateSecretWord():
    phraseGen = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": "Please respond with the name of an object."}
      ],
      temperature=1.5
    )

    secretPhrase = phraseGen.choices[0].message.content
    return secretPhrase


def DescribeScene(secretPhrase):
    sceneGen = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"In the response, do not use the word {secretPhrase}, only describe the scene. Keep the response short, like 'a gas station' or 'a rainforest'."},
        {"role": "user", "content": f"First, think of somewhere you wouldn't expect to find a {secretPhrase}. Then, describe that place. "}
      ],
      max_tokens=100,
      temperature=1
    )
    scene = sceneGen.choices[0].message.content
    return scene
    


def GenerateImage(secretPhrase, scene):
    try:
        imageResponse = openai.Image.create(
          prompt=f"{scene} with a {secretPhrase} in it, detailed photo",
          n=1,
          size="1024x1024"
        )
        imageURL = imageResponse.data[0].url
        return imageURL
    except openai.error.OpenAIError() as e:
        print(e.http_status)
        print(e.error)
    

secretPhrase = GenerateSecretWord()
print("secret phrase: " + secretPhrase)

scene = DescribeScene(secretPhrase)
print("Scene: " + scene)

imageURL = GenerateImage(secretPhrase, scene)
print(imageURL)
webbrowser.open(imageURL, new=0)

print("Based on the image, what object am I thinking of?")
userGuess = input()

if(userGuess == secretPhrase)
    print("Wow, that's exactly correct!")
    GameEnd()

# use embeddings to test user's guess's similarity to actual word. allow user to choose to generate another image or 
# guess again. Maybe generating a second image loses points? Maybe also allow asking for a text clue?


    