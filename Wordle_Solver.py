import numpy as np
import string
import random
import os


def getListOfWords():
    dictionary_path = os.getcwd()
    dictionary = open(dictionary_path + "/wordle_dictionary", "r")  # get dictionary for Wordle
    dictionary_words = dictionary.readlines()
    word_list = [w.rstrip() for w in dictionary_words]      #remove the '\n' character at the end of each word
    return word_list


class WordleSolver:

    def __init__(self, word_list, green_list, green_list_pos, yellow_list, yellow_list_pos, black_list):
        
        self.word_list = word_list
        self.green_list = green_list
        self.green_list_pos = green_list_pos
        self.yellow_list = yellow_list
        self.yellow_list_pos = yellow_list_pos
        self.black_list = black_list

        self.letter_count = dict.fromkeys(string.ascii_lowercase, 0)    #dict that stores count of each letter 

        new_list = self.reduceWordList()
        guess_list = self.getBestGuesses(new_list)
        
        print("########################################################")

        print('Number of possible words = ' + str(len(new_list)))

        if len(new_list) <= 7 :
            print('List of possible words = ' + str(new_list))

        print('Number of best guesses = ' + str(len(guess_list)))

        if guess_list:
            print('best guess : ' + random.choice(guess_list))
        else:
            print("NO POSSIBLE WORD !!!")
            exit()

        print("########################################################")


    #Get a reduced list of words after applying black_list, green_list, yellow_list
    def reduceWordList(self):
        
        new_list = []

        for word in self.word_list:

            word_possible = True

            for letter, index in zip(word, range(5)):
                if letter in self.black_list:
                    if letter in self.green_list or letter in self.yellow_list:     #Check for repeated letters in word
                        for l, i in zip(word, range(5)):
                            if l == letter and i != index :
                                word_possible = False
                    else:
                        word_possible = False
                        break

            for green_letter, letter_pos in zip(self.green_list, self.green_list_pos) :
                if word[letter_pos] != green_letter :
                    word_possible = False
                    break  

            for yellow_letter, letter_pos in zip( self.yellow_list, self.yellow_list_pos) :
                if yellow_letter not in word or word[letter_pos] == yellow_letter :
                    word_possible = False
                    break
            
            if word_possible == True:
                new_list.append(word)
        
        return new_list

    # Get the best guess for next word based on current word list
    def getBestGuesses(self, ori_word_list):
        
        guess_list = []
        max_count = 0
        
        for word in ori_word_list:
            letter_counted = []
            for letter, index in zip(word, range(5)) :
                if letter not in letter_counted:   #To prevent giving preference to duplicate letters in the word
                    letter_counted.append(letter) 
                    self.letter_count[letter] += 1
        
        for word in ori_word_list:
            
            word_count = 0
            
            for letter in word :  
                word_count += self.letter_count[letter]

            if word_count == max_count :
                guess_list.append(word)

            if word_count > max_count :
                guess_list = []
                guess_list.append(word)
                max_count = word_count
            
        return guess_list

    
if __name__ == "__main__":
    
    word_list = getListOfWords()

    green_list = []
    green_list_pos = []
    yellow_list = []
    yellow_list_pos = []
    black_list = []

    print("First enter the word with correct letters. Use caps for green spaces and lower case for yellow spaces.")
    print("Enter any other special character in place of the black spaces.")
    print("Next follow the prompt to enter all black space letters as a single string. No need to include the older letters.")
    print("#################################################################################################################")
    print('Best First Guess: SOARE')
    print("########################################################") 

    while True:
        
        
        input_word = raw_input('Enter the Word: ')
        reject_letters = raw_input('Enter black spaced letters: ')

        for letter, index in zip(input_word, range(5)):
            
            if letter.isupper():
                green_list.append(letter.lower())
                green_list_pos.append(index)
            
            if letter.islower():
                yellow_list.append(letter)
                yellow_list_pos.append(index)
        
        for letter in reject_letters:
            black_list.append(letter)

        w = WordleSolver(word_list, green_list, green_list_pos, yellow_list, yellow_list_pos, black_list)

        end_game = raw_input('End Game? (n/y)   ')
        
        if end_game == 'y':
            
            new_game = raw_input('New Game? (n/y)   ')
            
            if new_game == 'n': exit()

            green_list = []
            green_list_pos = []
            yellow_list = []
            yellow_list_pos = []
            black_list = []

            os.system('clear')

            print('Best First Guess: SOARE')
            print("########################################################") 

         