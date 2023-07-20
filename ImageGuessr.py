import os
import openai
import numpy as np
import webbrowser

openai.api_key = os.getenv("OPENAI_API_KEY")

# Global variables
completionModel = "gpt-3.5-turbo"
embeddingModel = "text-embedding-ada-002"
debug = True

def SetupNewGame():
    global points
    global totalPoints
    global frame
    global firstGuess
    global secretPhrase
    firstGuess = True
    totalPoints = 0
    points = 10
    frame = 1
    print("New game started.")
    secretPhrase = GenerateSecretWord()
    if(debug): print("secret phrase: " + secretPhrase)

    # scene = DescribeScene(secretPhrase)
    # if(debug): print("Scene: " + scene)

    # imageURL = GenerateImage(secretPhrase, scene)
    # if(debug): print(imageURL)
    # webbrowser.open(imageURL, new=0)

    print("Based on the image, what object am I thinking of?")
    AskForGuess()
    
def NewFrame():
    global totalPoints
    global frame
    global firstGuess
    global similarity
    global lastSimilarity
    totalPoints += points
    frame += 1
    firstGuess = True
    similarity = -2
    lastSimilarity = -2
    print(f'you made {points} points! Your score is now {totalPoints}, and we are on frame {frame}')

def AskForGuess():
    global secretPhrase
    userGuess = input("Your guess: ")
    CheckGuess(userGuess, secretPhrase)
    
def CheckGuess(guess, secretPhrase):
    global points
    global firstGuess
    global similarity
    global lastSimilarity
    
    if(GuessIsCorrect(guess, secretPhrase)): # Correct guess
        if(firstGuess):
            print("Wow, that's correct! First try!")
        else:
            print("That's correct!")
        NewFrame()
    else: # Incorrect guess
        similarity = DetermineCloseness(guess, secretPhrase)
        if(not firstGuess):
            if(lastSimilarity < similarity):
                print("You're getting closer...")
            else:
                print("Your previous guess was better.")
        lastSimilarity = similarity
        firstGuess = False
        print("Guess again?")
        guessAgainInput = input()
        if(guessAgainInput == "y" or "yes" or "true"):
            points -= 1
            AskForGuess()
        else:
            GameEnd()
    
def GuessIsCorrect(guess, secretPhrase):
    return guess.upper() == secretPhrase.upper()
    
def DetermineCloseness(guess, secretPhrase):
    embeddingsToCompare = openai.Embedding.create(
    input=[guess, secretPhrase],
    model=embeddingModel
    )
    guessVector = embeddingsToCompare['data'][0]['embedding']
    secretPhraseVector = embeddingsToCompare['data'][1]['embedding']
    
    #similarityScore will be between -1 and 1, higher means more similar
    similarityScore = np.dot(guessVector, secretPhraseVector)
    if(debug): print(f"similarity score: {similarityScore}")
    return similarityScore
        
def GameEnd():
    print(f"Game Over! Your score: {totalPoints}")
    SetupNewGame()

def GenerateSecretWord():
    phraseGen = openai.ChatCompletion.create(
      model=completionModel,
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
      model=completionModel,
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
    
SetupNewGame()
# use embeddings to test user's guess's similarity to actual word. allow user to choose to generate another image or 
# guess again. Maybe generating a second image loses points? Maybe also allow asking for a text clue?


    