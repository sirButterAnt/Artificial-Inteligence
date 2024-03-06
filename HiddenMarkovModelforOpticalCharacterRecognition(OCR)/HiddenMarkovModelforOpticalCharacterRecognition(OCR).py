def read_file_and_create_list(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read all lines from the file and store them in a list
            lines = file.readlines()
            
            # Optional: Remove newline characters from each line
            lines = [line.strip() for line in lines]
            
            return lines
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
file_path1 ='C:\\Users\\Zeynep\\Desktop\\Ceng 461\\HW2\\data_actual_words.txt'  # Replace with the path to your text file
actualWords = read_file_and_create_list(file_path1)

file_path2 ='C:\\Users\\Zeynep\\Desktop\\Ceng 461\\HW2\\data_ocr_outputs.txt'  # Replace with the path to your text file
OCR_words = read_file_and_create_list(file_path2)




initialProbability = {chr(letter): 0 for letter in range(ord('A'), ord('Z') + 1)}


# Display the dictionary
print(initialProbability )
total_lines_processed = 50000
for index in range(0,total_lines_processed):
        if actualWords[index] and 'A' <= actualWords[index][0] <= 'Z':
            initialProbability[actualWords[index][0] ] += 1



for key in initialProbability :
    initialProbability [key] /= total_lines_processed




#initial state probabilities
print("initial state probabilities")

for key in initialProbability:
    print(f"Key: {key}, Value: {initialProbability[key]}")



transitionProbability = {}

for letter in range(ord('A'), ord('Z') + 1):
    sub_dict = {}
    sub_dict["count"] = 0
    for sub_letter in range(ord('A'), ord('Z') + 1):
        sub_dict[chr(sub_letter)] = 0
    transitionProbability[chr(letter)] = sub_dict

# Display the dictionary

max_words = 50000
processed_words = 0

for word in actualWords:
    for i in range(len(word) - 1):
        current_letter = word[i].upper()
        next_letter = word[i + 1].upper()
        transitionProbability[current_letter][next_letter] += 1
        transitionProbability[current_letter]["count"] +=1
    
    processed_words += 1
    if processed_words >= max_words:
        break


for key in transitionProbability :
    for nextState in transitionProbability[key]:
        if (nextState != "count"):
            transitionProbability[key][nextState] /= transitionProbability[key]["count"]
    transitionProbability[key].pop("count")

print("transitionProbability")
for key in transitionProbability:
    print("\n")
    print(f"Transiton Key: {key}, Value: {transitionProbability[key]}")





emittanceProbability = {}

for letter in range(ord('A'), ord('Z') + 1):
    sub_dict = {}
    sub_dict["count"] = 0
    for sub_letter in range(ord('A'), ord('Z') + 1):
        sub_dict[chr(sub_letter)] = 0
    emittanceProbability[chr(letter)] = sub_dict



for index in range(0, 50000):
        for charIndex in range(len(actualWords[index]) ):
            actual_letter = actualWords[index][charIndex].upper()
            oct_letter = OCR_words[index][charIndex].upper()
            emittanceProbability[actual_letter][oct_letter] += 1
            emittanceProbability[actual_letter]["count"] +=1


for key in emittanceProbability:
    for nextState in emittanceProbability[key]:
        if (nextState != "count"):
            emittanceProbability[key][nextState] /= emittanceProbability[key]["count"]
    emittanceProbability[key].pop("count")

print("\n emittance probability")
for key in emittanceProbability :
    print("\n")
    print(f"Emittion Key: {key}, Value: {emittanceProbability[key]}")


#likelihood  

def viterbi(ocrWord):
    
    currentWordsProb = {chr(letter): ["", 0] for letter in range(ord('A'), ord('Z') + 1)}
    
    if len(ocrWord) == 1:
        for currentLetter in currentWordsProb:
            currentWordsProb[currentLetter][0] = currentLetter
            currentWordsProb[currentLetter][1] = initialProbability[currentLetter] * emittanceProbability[currentLetter][ocrWord]
        return currentWordsProb
    

    previousDictionary = viterbi(ocrWord[:-1])
    for currentLetter in currentWordsProb: 
        for previousLetter in currentWordsProb:
            probability = previousDictionary[previousLetter][1]  * transitionProbability[previousLetter][ currentLetter] * emittanceProbability[currentLetter][ ocrWord[-1]]
            if probability > currentWordsProb[currentLetter][1]:
                currentWordsProb[currentLetter][0] = previousDictionary[previousLetter][0] + currentLetter
                currentWordsProb[currentLetter][1] = probability
    return currentWordsProb
            

  


def numberOfCorrected(new, ocr, actual):
    length = len(new)
    count = 0
    if (length == len(ocr)):
        for index in range(length):
            if new[index] != ocr[index] and new[index] == actual[index]:
                count += 1
    return count

def changePrinter(ocrWord, viterbiWord,):
    boolean = True
    for i in range(len(ocrWord)):
        if ocrWord[i] != viterbiWord[i]:
            boolean = False
            break
    if (boolean == False):
        print(f"Ocr Word: {ocrWord}, Viterbi Word:{ ''.join(viterbiWord)} ")

def mostProbable(dictionary):
    max = 0
    word = ""
    for key in dictionary:
        if dictionary[key][1] > max:
            max = dictionary[key][1] 
            word = dictionary[key][0]
    return max, word

count = 0
countOfChanged = 0
for wordIndex in range(50001, 60244): 
    ocr_word = OCR_words[wordIndex]
    viterbiWord = mostProbable(viterbi(ocr_word))[1]
    count += numberOfCorrected(viterbiWord, ocr_word, actualWords[wordIndex])
    
    boolean = True
    for i in range(len(ocr_word)):
        if ocr_word[i] != viterbiWord[i]:
            boolean = False
            break
    if (boolean == False):
        countOfChanged += 1
        print(f" Count: {countOfChanged} Ocr Word: {ocr_word}        Viterbi Word:{ ''.join(viterbiWord)} ")
        


print("number of corrected changed letters  " + str(count))

