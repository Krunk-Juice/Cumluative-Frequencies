# CPSC 535 Advanced Algorithms
# Project 2: Cumulative Frequencies
# Christopher Ta     cta002@csu.fullerton.edu
# Sicheng Long       xlongx@csu.fullerton.edu
# William Lee        leewilliam4@csu.fullerton.edu

import re

def split_text(filename):
    file_object = open(filename)
    word_frequencies = file_object.readline()
    WF = []
    
    #Get rid of excess punctuations
    word_frequencies = re.sub('[({""})]','',word_frequencies)
    #split at commas
    word_frequencies = word_frequencies.split(",")
    word_frequencies[-1] = word_frequencies[-1].strip()    
    
    sizeWF = len(word_frequencies)
    
    #delete spaces before and after the word(s)
    for i in range(sizeWF):
        word_frequencies[i] = word_frequencies[i].strip()
    
    #append them to WF in 2D array
    for j in range(0,len(word_frequencies),2):
        WF.append((word_frequencies[j],word_frequencies[j+1]))
    
    
    # output WF[]
    print("Words_Frequencies: WF[] =", WF, "of size", len(WF), "\n")
    
    #read the 2nd line, and get LS[]
    synonym_content = file_object.readline()
    SYN = []
    
    #parse Synonyms. Get rid of punctuations
    synonym_content = re.sub('[({""})]','',synonym_content)
    #split
    synonym_content = synonym_content.split(",")

    sizeSYN = len(synonym_content)
    
    #strip spaces
    for s in range(sizeSYN):
        synonym_content[s] = synonym_content[s].strip()
    #put into 2d array
    for t in range(0,len(synonym_content),2):
        SYN.append((synonym_content[t],synonym_content[t+1]))

    #output original SYN
    print("Synonyms: SYN[] =", SYN, "of size", len(SYN))
    
    file_object.close()
    return (WF, SYN)

def string_to_number(word_frequencies):
    words = []
    for a in range(len(word_frequencies)):
        words.append((word_frequencies[a][0], int(word_frequencies[a][1])))
    return words

# The function to output the final results
def cumulative_frequencies(frequencies_list, sorted_synonym_group):
    word_frequencies = []
    CF = []

    for i in range(len(sorted_synonym_group)):
        primary_word = sorted_synonym_group[i][0]
        total_frequency = 0
        # for j in sorted_synonym_group[i]:
        for k in range(len(frequencies_list)):
            if frequencies_list[k][0] in sorted_synonym_group[i]:
                total_frequency = total_frequency + frequencies_list[k][1]
        word_frequencies.append(primary_word)
        word_frequencies.append(total_frequency)
    
    for j in range(len(word_frequencies)//2):
        CF_pair = (word_frequencies[2*j], word_frequencies[2*j + 1])
        CF.append(CF_pair)

    return CF

# Group synonyms together    
def synonym_group(synonym_list):
    L = []
    added = []
    for i in range(len(synonym_list)):   # mark all synonym pairs are not addded
        added.append(False)
    for i in range(len(synonym_list)):
        if added[i] == False:    # only check the synonym pairs are not recorded
            S = []
            S.append(synonym_list[i][0])
            S.append(synonym_list[i][1])
            added[i] = True
            k = 0
            while k != len(S):
                k = len(S)
                for j in range(i+1, len(synonym_list)):
                    if synonym_list[j][0] in S:
                        if S.count(synonym_list[j][1]) == 0:
                            S.append(synonym_list[j][1])
                            added[j] = True
                    if synonym_list[j][1] in S:
                        if S.count(synonym_list[j][0]) == 0:
                            S.append(synonym_list[j][0])
                            added[j] = True
            L.append(S)
    
    # Prune excess
    # O(n^4) time complexity
    for i in range(0, len(L) - 1):
        for j in range(i + 1, len(L)):
            excess = False
            for k in range(len(L[i])):
                for l in range(len(L[j])):
                    # print(L[i][k], " compare to ", L[j][l])
                    if L[i][k] == L[j][l]:
                        excess = True
                        break
                if excess:
                    break
            if excess:
                del L[j]
                break
    return(L)


# This is the sorting for alphabetical output
# O(n^4) time complexity
def alphabetical_sort(synonym_list):
    words = synonym_list
    for i in range(0, len(synonym_list)):
        for a in range(0, len(words[i]) - 1):
            min_index = a
            for b in range(a + 1, len(words[i])):
                for c in range(min(len(words[i][min_index]), len(words[i][b]))):
                    if words[i][b][c] == words[i][min_index][c]:
                        if c == min(len(words[i][min_index]), len(words[i][b])) and len(words[i][b]) < len(words[i][min_index]):
                            min_index = b
                    elif words[i][b][c] < words[i][min_index][c]:
                        min_index = b
                        break
                    else:
                        break
            temp = words[i][a]
            words[i][a] = words[i][min_index]
            words[i][min_index] = temp

    return words    # Returns sorted 


if __name__ == '__main__':
    filename = input("Please enter the file name:")
    print()
    print("Input:")
    text_list = split_text(filename)
    word_frequencies = string_to_number(text_list[0])
    grouped = synonym_group(text_list[1])
    sorted_grouped = alphabetical_sort(grouped)
    CF = cumulative_frequencies(word_frequencies, sorted_grouped)
    
    print()
    print("Output:")
    print("CF[] =", CF, "size of", len(CF))
