#!/usr/bin/env python3

# ---------------------------------------------------------------
#
# CMPUT 331 Student Submission License
# Version 1.0
# Copyright 2026 Albert Ganut
#
# Redistribution is forbidden in all circumstances. Use of this software
# without explicit authorization from the author is prohibited.
#
# This software was produced as a solution for an assignment in the course
# CMPUT 331 - Computational Cryptography at the University of
# Alberta, Canada. This solution is confidential and remains confidential
# after it is submitted for grading.
#
# Copying any part of this solution without including this copyright notice
# is illegal.
#
# If any portion of this software is included in a solution submitted for
# grading at an educational institution, the submitter will be subject to
# the sanctions for plagiarism at that institution.
#
# If this software is found in any public website or public repository, the
# person finding it is kindly requested to immediately report, including
# the URL or other repository locating information, to the following email
# address:
#
#          gkondrak <at> ualberta.ca
#
# ---------------------------------------------------------------

"""
Assignment 7
Author: Albert Ganut
"""

from sys import flags
import math
import os

def read_text(filename):

    with open(filename, "r", encoding = "utf-8") as file:
        text = file.read()

    return text

def calculate_SSD(text):

    text = text.upper()
    letter_counts = {} # this is the dictionary that will hold the counts of each letter    
    total_letters = 0

    for letter in text:

        # if the current character is a letter and it's not already in the dictionary, then it adds it. If it's already in the dictionary then it increments its count and the total letter count
        if letter.isalpha():
            if letter not in letter_counts:
                letter_counts[letter] = 0

            letter_counts[letter] += 1
            total_letters += 1

    distribution = [] # this list will hold the frequencies of each letter in the text, sorted in descending order

    # if there are no letters (e.g., "123"), then it just returns an empty list. Otherwise, it sorts the letters by their counts in descending order and calculates the frequency of each letter
    if total_letters == 0:

        return distribution # returns early so that it also doesn't attempt to divide by zero

    sorted_letters_counts = sorted(letter_counts.values(), reverse=True)

    for count in sorted_letters_counts:
        
        prob = count / total_letters # this is how it gets the frequency (e.g., "A" appears 5 times in a text of 100 letters, so the frequency is 5/100 = 0.05)
        distribution.append(prob)

    return distribution

def calculate_SSD_distance(distribution1, distribution2 ):

    distance = 0.0 # this is the distance between two distributions
    length = max(len(distribution1), len(distribution2)) # we get the bigger length of the two distributions so that we can iterate through both of them if one is longer

    for i in range(length):
        
        prob1 = 0.0
        prob2 = 0.0

        # checks if the index is within the bounds of the distribution. If so, then it gets the probability at that index. If not, then it just leaves the probability as 0.0
        if i < len(distribution1):
            prob1 = distribution1[i]

        # similarly here
        if i < len(distribution2):
            prob2 = distribution2[i]

        prob_difference = prob1 - prob2 # this calculates how far apart the two probabilities are at that index (e.g., 0.05 - 0.02 = 0.03)
        distance += prob_difference ** 2 # we square the difference so that negatives don't cancel out positives and then add it to the distance

    return distance

def calculate_DPD(text):

    text = text.upper()
    words = text.split()

    pattern_counts = {} # this dictionary will track how many words have each pattern

    for word in words:

        letter_counts = {} # this dictionary will hold the count for each letter in the current word

        for letter in word:

            # if the current character in the word is a letter and it's not already in the dictionary, then it adds it. If it's already in the dictionary then it increments its count
            if letter.isalpha():
                if letter not in letter_counts:
                    letter_counts[letter] = 0

                letter_counts[letter] += 1

        sorted_counts = sorted(letter_counts.values(), reverse=True) # this sorts the counts of the letters in the current word in descending order (e.g., "hello" would have counts of [2, 1, 1, 1] for "l", "h", "e", and "o" respectively)
        pattern = tuple(sorted_counts) # this converts the sorted counts into a tuple so that it can be used as a key in the pattern_counts dictionary

        # if the current pattern isn't already in the pattern_counts dictionary, then it adds it with a count of 0. Then it increments the count for that pattern
        if pattern not in pattern_counts:
            pattern_counts[pattern] = 0

        pattern_counts[pattern] += 1

    distribution = {}
    total_words = len(words)

    # if there are no words then we just return early with an empty dictionary
    if total_words == 0:

        return distribution

    # if there are words then we calculate the frequency of each pattern by dividing the count of that pattern by the total number of words
    for pattern in pattern_counts:

        distribution[pattern] = pattern_counts[pattern] / total_words

    return distribution

def calculate_DPD_distance(distribution1, distribution2):

    # this adds all the patterns from both dictionaries into a set. It's stored in a set so that all duplicates are removed --> each pattern is only stored once)
    all_patterns = set(distribution1.keys())
    all_patterns.update(distribution2.keys())

    distance = 0.0
    
    for pattern in all_patterns:

        # this gets the probabilities of the current pattern from both distributions. If the pattern isn't in one of the distributions, then it just returns 0.0 for that distribution
        # e.g., if distribution1 has the pattern (2, 1) with a probability of 0.05 and distribution2 doesn't have that pattern, then prob1 = 0.05 and prob2 = 0.0
        prob1 = distribution1.get(pattern, 0.0)
        prob2 = distribution2.get(pattern, 0.0)

        # finds the distance between the two probabilities for the current pattern, squares it (so the subtraction order doesn't matter), and then adds it to the total distance    
        prob_difference = prob1 - prob2 
        distance += prob_difference ** 2

    return distance

def cliSSD(ciphertext: str, files):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """

    ciphertext_distribution = calculate_SSD(ciphertext)
    distances = {}

    for filename in files:

        sample_text = read_text(filename)
        sample_distribution = calculate_SSD(sample_text)

        distance = calculate_SSD_distance(ciphertext_distribution, sample_distribution)
        distances[filename] = distance

    return distances

def cliDPD(ciphertext: str, files):
    """
    Args:
        ciphertext (str)
        files (list of str)
    Returns:
        dict
    """
    ciphertext_distribution = calculate_DPD(ciphertext)
    distances = {}

    for filename in files:

        sample_text = read_text(filename)
        sample_distribution = calculate_DPD(sample_text)

        distance = calculate_DPD_distance(ciphertext_distribution, sample_distribution)
        distances[filename] = distance

    return distances

def cliSSDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """

    predictions = {}

    if len(ciphertext_files) == 0:

        return predictions

    if len(sampletext_files) == 0:

        raise ValueError("You need at least one sample text file!")

    sample_distributions = {}

    for sample_file in sampletext_files:    

        sample_text = read_text(sample_file)
        sample_distributions[sample_file] = calculate_SSD(sample_text)

    for ciphertext_file in ciphertext_files:    

        ciphertext = read_text(ciphertext_file)
        ciphertext_distribution = calculate_SSD(ciphertext) 

        smallest_distance = float("inf")
        best_match = None

        for sample_file in sampletext_files:

            sample_distribution = sample_distributions[sample_file]
            distance = calculate_SSD_distance(ciphertext_distribution, sample_distribution)

            if distance < smallest_distance:
                smallest_distance = distance
                best_match = sample_file

        predictions[ciphertext_file] = best_match

    return predictions

def cliDPDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """

    predictions = {}

    if len(ciphertext_files) == 0:

        return predictions

    if len(sampletext_files) == 0:

        raise ValueError("You need at least one sample text file!")

    sample_distributions = {}

    for sample_file in sampletext_files:    

        sample_text = read_text(sample_file)
        sample_distributions[sample_file] = calculate_DPD(sample_text)

    for ciphertext_file in ciphertext_files:    

        ciphertext = read_text(ciphertext_file)
        ciphertext_distribution = calculate_DPD(ciphertext) 

        smallest_distance = float("inf")
        best_match = None

        for sample_file in sampletext_files:

            sample_distribution = sample_distributions[sample_file]
            distance = calculate_DPD_distance(ciphertext_distribution, sample_distribution)

            if distance < smallest_distance:
                smallest_distance = distance
                best_match = sample_file

        predictions[ciphertext_file] = best_match

    return predictions

def generateMapping(dictionary: dict):
    """
    Args:
        dictionary (return value of cliSSDTest or cliDPDTest)
    Returns:
        A classification mapping (dict) of the ciphertexts.
        Please refer to the assignment instructions for the required format.
    """

    mapping = {}

    for ciphertext_file in dictionary:

        sample_file = dictionary[ciphertext_file]

        actual_file = os.path.basename(ciphertext_file)
        actual_name = os.path.splitext(actual_file)[0]  
        actual_language = actual_name.split("_")[1]

        predicted_file = os.path.basename(sample_file)
        predicted_name = os.path.splitext(predicted_file)[0]
        predicted_language = predicted_name.split("_")[1]

        language_pair = (actual_language, predicted_language)

        if language_pair not in mapping:
            mapping[language_pair] = 0

        mapping[language_pair] += 1

    return mapping

def generateMatrix(mapping):
    """
    Args:
        mapping (dictionary returned by generateMapping)
    Returns:
        None (prints a formatted confusion matrix)
    """
    languages = ["bg", "de", "el", "en", "es", "fr", "it", "nl", "pl", "ru"]

    header = "     " + " | ".join(languages)
    print("\n")
    print(header)
    print("   " + "-" * len(header))

    for actual in languages:
        row = [f"{mapping.get((actual, predicted), 0):>2}" for predicted in languages]
        print(f"{actual} | {' | '.join(row)}")
    print("\n") 

def evaluate_all_ciphertexts():

    languages = ["bg", "de", "el", "en", "es", "fr", "it", "nl", "pl", "ru"]    

    ciphertext_files = []
    sampletext_files = []   

    for language in languages:
        sample_file = os.path.join("texts", f"sample_{language}.txt")
        sampletext_files.append(sample_file)

        for number in range(1, 6):

            ciphertext_file = os.path.join("texts", f"ciphertext_{language}_{number}.txt")
            ciphertext_files.append(ciphertext_file)

    ssd_predictions = cliSSDTest(ciphertext_files, sampletext_files)
    dpd_predictions = cliDPDTest(ciphertext_files, sampletext_files)

    ssd_mapping = generateMapping(ssd_predictions)
    dpd_mapping = generateMapping(dpd_predictions)

    print("Confusion Matrix for SSD: ")
    generateMatrix(ssd_mapping)

    print("Confusion Matrix for DPD: ")
    generateMatrix(dpd_mapping)

    ssd_correct = 0
    dpd_correct = 0

    for language in languages:
        ssd_correct += ssd_mapping.get((language, language), 0)
        dpd_correct += dpd_mapping.get((language, language), 0)

    total = len(ciphertext_files)

    print(f"SSD Accuracy: {ssd_correct}/{total}")
    print(f"DPD Accuracy: {dpd_correct}/{total}") 

def test():

# Test cases for Problem 1 and Problem 2.
# Results are compared using math.isclose and pass if within 0.0008
# of the expected value (Python's sum() may round the last digits differently).
# Feel free to add more test cases here 
    cipher = """fukvuvu osyxhwuyxg wxhobsuv gxrxvbepxsy ucybsbpbck ewbixty povvobs xtc ybyuv tbky povvobs xtc
ylx xcwbexus gopxskobs luwpbsokosh bdixtyorxk kywctycwuv mcsgk xntlushosh osmbwpuyobs xnexwoxstx usg ogxuk tbvvudbwuyorx fbwa pbsoybwosh kbtouv euwysxwk v
xcwbexus tbppokkobs
xcwbexus gxtokobsk bs ylx opevxpxsyuyobs bmylx tbppbs kxtcwoyj usg gxmxstx ebvotj ostvcgosh ylbkx osoyouyosh u pokkobs uk wxmxwwxg yb os ylok uwyotvx kluvv dx ugbeyxg dj ylx tbcstov bm posokyxwk utyosh csusopbckvj bs u ewbebkuv mwbp ylx csobs posokyxw mbw mbwxohs ummuowk bw mwbp u pxpdxw kyuyx
oo yb xskcwx yluy ylx xcwbexus ewbebkuv vosxk mwupxk exw kxtbsg ewbhwxkkorx ktussosh ok ugbeyxg uk ylx koshvx fbwvg kyusg uwg
ylx pbwx xmmotoxsy ylx bexwuybwk osrbvrxg ylx pbwx xmmotoxsy ylx xcwbexus yxvxtbppcsotuyobsk puwaxy fovv dx
yuos ylx ybyuv ruvcx bm ylx wxkeowuyovx gcky tbstxsywuyobs mbw kextomoxg yopx osyxwruvk
oyv
dj vxyyxw guyxg puwtl gw gx gbposotok fuk osmbwpxg dj gh nro yluy ylx ewbixty bm ylx mbcsguyobs lug sby dxxs kxvxtyxg dxtuckx oy gog sby pxxy ylx ussbcstxg twoyxwou
bs yb sbrxpdxw os tbsicstyobs foyl ylx sxylxwvusgk posokywj bm lxuvyl usg ylx xsrowbspxsy ylx tbppokkobs lxvg us osyxwsuyobsuv tbsmxwxstx uy ylx luhcx bs tvxus yxtlsbvbhoxk bkuv yb ylx tbcstov tbstxwsosh u pcvyousscuv ewbhwuppx os ylx moxvg bm dobpbvxtcvuw xshosxxwosh osgowxty utyobs ylx xtbsbpot usg kbtouv tbppoyyxx pxxyosh bs usg sbrxpdxw gxvorxwxg us beosobs bs ylx tbppokkobs ewbebkuv yb ylx tbcstov tbstxwsosh cwusocp xnevbwuyobs usg xnywutyobs osgowxty utyobs
"""
    a = cliSSD(cipher, ["texts/sample_bg.txt", "texts/sample_de.txt", "texts/sample_el.txt", "texts/sample_en.txt", "texts/sample_es.txt", "texts/sample_fr.txt", "texts/sample_it.txt", "texts/sample_nl.txt", "texts/sample_pl.txt", "texts/sample_ru.txt"])
    expected_a = {'texts/sample_bg.txt': 0.0008686304175672087, 'texts/sample_de.txt': 0.0030282241681359465, 'texts/sample_el.txt': 0.003900768672618399, 'texts/sample_en.txt': 0.0009685983479506998, 'texts/sample_es.txt': 0.0014847832596343855, 'texts/sample_fr.txt': 0.002342377137372695, 'texts/sample_it.txt': 0.0008613778129189986, 'texts/sample_nl.txt': 0.00658594015644843, 'texts/sample_pl.txt': 0.004795508346043341, 'texts/sample_ru.txt': 0.002884312599878665}
    for k in expected_a:
        assert math.isclose(a[k], expected_a[k], abs_tol=0.0008), f"{k}: got {a[k]}, expected {expected_a[k]}"

    b = cliDPD(cipher, ["texts/sample_bg.txt", "texts/sample_de.txt", "texts/sample_el.txt", "texts/sample_en.txt", "texts/sample_es.txt", "texts/sample_fr.txt", "texts/sample_it.txt", "texts/sample_nl.txt", "texts/sample_pl.txt", "texts/sample_ru.txt"])
    expected_b = {'texts/sample_bg.txt': 0.03760706244775398, 'texts/sample_de.txt': 0.019627307148711397, 'texts/sample_el.txt': 0.010778849211054852, 'texts/sample_en.txt': 0.004254877302061767, 'texts/sample_es.txt': 0.017505446082276693, 'texts/sample_fr.txt': 0.0120039286951674, 'texts/sample_it.txt': 0.01241955510016762, 'texts/sample_nl.txt': 0.009751349385997449, 'texts/sample_pl.txt': 0.03375909319348446, 'texts/sample_ru.txt': 0.03334088648579243}
    for k in expected_b:
        assert math.isclose(b[k], expected_b[k], abs_tol=0.0008), f"{k}: got {b[k]}, expected {expected_b[k]}"

    evaluate_all_ciphertexts()

if __name__ == "__main__" and not flags.interactive:
    test()