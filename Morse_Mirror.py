"""
Morse Encoder and Decoder with GUI

Written by Ethan Sim
"""

import re
import tkinter

##Dictionary

#Let's begin by creating the dictionary
morse_dict = {" ":"/ ", "A":".- ", "B":"-... ", "C":"-.-. ", "D":"-.. ", "E":". ", "F":"..-. ", "G":"--. ", 
              "H":".... ", "I": ".. ", "J":".--- ", "K":"-.- ", "L":".-.. ", "M":"-- ", "N":"-. ", "O":"--- ",
              "P":".--. ", "Q":"--.- ", "R":".-. ", "S":"... ", "T":"- ", "U":"..- ", "V":"...- ", "W":".-- ",
              "X":"-..- ", "Y":"-.-- ", "Z":"--.. ", "1":".---- ", "2":"..--- ", "3":"...-- ", "4":"....- ",
              "5":"..... ", "6":"-.... ", "7":"--... ", "8":"---.. ", "9":"----. ", "0":"----- ", ".":".-.-.- ",
              ",":"--..-- ", "?":"..--.. ", "'":".----. ", "!":"-.-.-- ", "/":"-..-. ", "(":"-.--. ", ")":"-.--.- ",
              "&":".-... ", ":":"---... ", ";":"-.-.-. ", "=":"-...- ", "+":".-.-. ", "-":"-....- ", "_":"..--.- ",
              '"':".-..-. ", "$":"...-..- ", "@":".--.-. "}

#Creating these lists to save memory when looking up values
plaintext_characters = list(morse_dict.keys())
ciphertext_characters = list(morse_dict.values())

##Encoding

#To refactor our code, let's use a helper function
def whitespace_sorter(sentence):
    """
    Takes as input a string sentence and removes leading and trailing whitespace, also coerces all multiple whitespaces into a single whitespace character.
    """
    sentence_copy = str(sentence)
    sentence_copy = sentence_copy.strip() #Remove leading and trailing whitespace (/s)
    sentence_copy = re.sub(" +", " ", sentence_copy) #Coerces all multiple /s characters into a single /s
    #It identifies a /s followed by any nonzero number of /s and replaces this with a single /s 
    return sentence_copy

def encode_morse(plaintext):
    """
    Takes as input a string plaintext and returns its Morse equivalent in string form.
    """
    if not isinstance(plaintext, str):
        return "Plaintext is not a string!"
    # Having confirmed it's a string, we convert it to uppercase - this will leave numbers and special characters untouched
    if not plaintext.isupper():
        plaintext_copy = plaintext.upper() #We don't want to mutate the input
    else:
        plaintext_copy = str(plaintext)
    plaintext_copy = whitespace_sorter(plaintext_copy)        
    ciphertext = "" #This also has the effect of returning an empty string if an empty string is the input
    #We then do the actual translation by simply looking up the dictionary value
    for character in plaintext_copy:
        if character not in plaintext_characters:
            return "ERROR: You can't encode the following character: " + character
        ciphertext += morse_dict[character]
    return ciphertext[:-1] #Remove trailing /s

#Testing encoder
def test_encoder():
    """
    This will run our Morse encoder against a selection of varying inputs, and compare the outputs to a model answer.
    """
    #Check edge cases first
    assert encode_morse(123) == "Plaintext is not a string!", "Test 1 failed, input integer 123"
    assert encode_morse("") == "", "Test 2 failed, input ''"
    assert encode_morse("^") == "ERROR: You can't encode the following character: ^", "Test 3 failed, input '^'"
    assert encode_morse("   e       e   ") == ". / .", "Test 4 failed, input '   e       e   '"
    assert encode_morse("AbCd") == ".- -... -.-. -..", "Test 5 failed, input 'AbCd'"
    
    #Now we run possible plaintexts and check their corresponding ciphertexts
    assert encode_morse("the quick brown fox jumps over the lazy dog") == "- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- -..- / .--- ..- -- .--. ... / --- ...- . .-. / - .... . / .-.. .- --.. -.-- / -.. --- --.", "Test 6 failed, input 'the quick brown fox jumps over the lazy dog'"
    assert encode_morse("H1er0ph@nT + '") == ".... .---- . .-. ----- .--. .... .--.-. -. - / .-.-. / .----.", "Test 7 failed, input 'H1er0ph@nT + ''"
    assert encode_morse('"' + "'") == ".-..-. .----.", "Test 8 failed, input ''(double apostrophe)' + '(single apostrophe)'"
    
    #Check that input not mutated
    test_plaintext_9 = "test"
    encode_morse(test_plaintext_9)
    assert test_plaintext_9 == "test", "Test 9 failed, input 'test' mutated"
    
    #If all tests passed
    print ("Congratulations! 9/9 tests passed!")

test_encoder()

##Decoding
def decode_morse(ciphertext):
    """
    Takes as input the Morse string ciphertext and returns a plaintext string.
    """
    if not isinstance(ciphertext, str):
        return "Ciphertext is not a string!"
    ciphertext_copy = str(ciphertext)
    if len(ciphertext) == 0: #Accounts for empty string
        return ""
    if ciphertext_copy[-1] != " ":
        ciphertext_copy += " " #Accounts for user variation in final trailing whitespace - we need this final whitespace for the dictionary to work
        #This also has the effect of returning nonsense characters we can't decode later on
    plaintext = "" #Empty string solution
    morse_char = "" #This variable will hold each letter/character's Morse code
    for character in ciphertext_copy:
        if character == " ": #Spaces are letter delimiters
            morse_char += character
            if morse_char in ciphertext_characters:
                plaintext += plaintext_characters[ciphertext_characters.index(morse_char)]
                morse_char = "" #Reset the holding variable
            else:
                return "ERROR: I can't decode the following character: " + morse_char + "\nYour decoded message thus far is: " + whitespace_sorter(plaintext)
                #The nature of this return statement allows tests via assertion, but will also respond to print statements accordingly.
        else:
            morse_char += character #If it's not a letter delimiter, continue building the letter/character Morse code
    plaintext = whitespace_sorter(plaintext)
    return plaintext

#Testing decoder
def test_decoder():
    """
     This will run our Morse decoder against a selection of varying inputs, and compare the outputs to a model answer.
    """
    #Check edge cases first
    assert decode_morse(123) == "Ciphertext is not a string!", "Test 1 failed, input integer 123"
    assert decode_morse("") == "", "Test 2 failed, input ''"
    assert decode_morse("string") == "ERROR: I can't decode the following character: string \nYour decoded message thus far is: ", "Test 3 failed, input 'string'"
    assert decode_morse(".- ..- / .- . .--.-.-.-.-.-.-.-.-.-.") == "ERROR: I can't decode the following character: .--.-.-.-.-.-.-.-.-.-. \nYour decoded message thus far is: AU AE", "Test 4 failed, input '.- ..- / .- . .--.-.-.-.-.-.-.-.-.-.'" 
    assert decode_morse("/") == "", "Test 5 failed, input '/'" #My function parses the slash as ciphertext, but whitespace_sorter discards it as meaningless noise.
    #This is fair because both encoder and decoder ignore spaces presented by themselves, in plaintext and ciphertext respectively.
    
    #Now we run possible ciphertexts and check their corresponding plaintexts:
    assert decode_morse("- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- -..- / .--- ..- -- .--. ... / --- ...- . .-. / - .... . / .-.. .- --.. -.-- / -.. --- --.") == "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", "Test 6 failed, input '- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- -..- / .--- ..- -- .--. ... / --- ...- . .-. / - .... . / .-.. .- --.. -.-- / -.. --- --.'"
    assert decode_morse(".... .---- . .-. ----- .--. .... .--.-. -. - / .-.-. / .----.") == "H1ER0PH@NT + '", "Test 7 failed, input '.... .---- . .-. ----- .--. .... .--.-. -. - / .-.-. / .----."
    assert decode_morse(".-..-. .----.") == '"' + "'", "Test 8 failed, input '.-..-. .----.'"
    
    #Check that input not mutated
    test_ciphertext_9 = "- . ... -"
    encode_morse(test_ciphertext_9)
    assert test_ciphertext_9 == "- . ... -", "Test 9 failed, input '- . ... -' mutated" 
    
    #If all tests passed
    print ("Congratulations! 9/9 tests passed!")

test_decoder()

##GUI creation

from tkinter import * #This gives us direct access to all public names within tkinter without needing to call tkinter.this, tkinter.that, etc.

morse_gui = Tk() #Initialises our GUI window - its name is morse_gui
morse_gui.title('Morse Translator') #Changes title

##First, we need some welcome text so the user knows what this is and what to do.

welcome_text = Text(morse_gui, height = 2, width = 100) #This is our text box
welcome_text.pack(side = TOP) #Our welcome text will be at the top of the window
welcome_text.insert("1.0","Welcome to my Morse Translator!\nSelect either Encode or Decode, put your message in, and hit Translate!") #Inserts at the first character (0) of the first line (1)

##Because we wrap two functions in a single GUI, we need mutually exclusive options - radio buttons will work best.

de_en_flag = StringVar() #Tell tkinter what type of variable this is: a StringVar object is a container which takes in strings
de_en_flag.set("encode") #We set this variable to have the value "encode" first, so we don't inadvertently fill both radio buttons - comment this out to see what I mean
Radiobutton(morse_gui, text = "Encode", variable = de_en_flag, value = "encode").pack(anchor = N, pady = (10,0)) #By clicking on the button, we change the value of de_en_flag
Radiobutton(morse_gui, text = "Decode", variable = de_en_flag, value = "decode").pack(anchor = N, pady = (0,10)) #Anchor controls where the text is postioned within morse_gui - options are N, NW, etc. and CENTER.
#The pady option takes in either a single integer or a tuple - adds the specified amount of vertical space to the top and bottom.

##After selecting their option, the user needs to know where to put their message in.

input_text = Text(morse_gui, height = 1, width = 23)
input_text.pack(side = TOP)
input_text.insert("1.0", "Put your message below!")

##We then create the space in which the user can put their message in.

user_input = Entry(morse_gui, width = 100)
user_input.pack(side = TOP, pady = 15)

##Now, we need to find some way of initiating the encoding or decoding process. 

def start_translator(de_en_flag): #This allows us to create conditional additions to the GUI
    if de_en_flag == "encode":
        output_text.replace("1.0", END, encode_morse(user_input.get())) #Removes all characters in the box (from 1.0 to the end) and puts the specified string in
    elif de_en_flag == "decode":
        output_text.replace("1.0", END, decode_morse(user_input.get()))
#Note that output_text (where the output will be displayed) has not been defined yet - this is okay, because the function has not yet been called.

##Skip this for now --------- (2)

#Since I now had two buttons of equal relevance to the user (who might want to run many encodes and decodes in sequence), I wanted to put them side-by-side in the centre.
#The best solution for this was to create a frame to hold them both, and position that frame between the user input and the output. This is where "code echoes order" helps a lot.
        
main_frame = Frame(morse_gui)
main_frame.pack(side = TOP)

##Now we need to let the user call start_translator. We need a start button.

start_button = Button(morse_gui, text = 'Translate!', width = 25, command = lambda: start_translator(de_en_flag.get())) 
#This lambda will use the StringVar object's get() method to return its current value, then pass it to start_translator
start_button.pack(in_ = main_frame, side = LEFT)

##Skip this for now --------- (1)

#After repeated usage, I needed some way to quickly remove large input messages, given the limited size of the user input box.

def clear_input():
    user_input.delete(0, END) #Clears user input box

clear_button = Button(morse_gui, text = 'Clear Message', width = 25, command = clear_input)
clear_button.pack(in_ = main_frame, side = RIGHT, padx = (20,0))

##We then need to display the output to the user.

output_text = Text(morse_gui, height = 10, width = 100)
output_text.pack(side = TOP, pady = 15)

##Finally, we need some way of neatly exiting the window.

exit_button = Button(morse_gui, text='Exit', width=25, command=morse_gui.destroy) #Adds exit button to terminate gui
exit_button.pack(side = TOP, pady = (0,15)) #Our exit button will be on the bottom of the window

##Once we're done, let's run the GUI!

morse_gui.mainloop() #This starts the GUI

## Go to point (1). 

## Go to point (2).
