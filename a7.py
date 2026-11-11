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

def calculate_SSD(text):

    text = text.upper()
    letter_counts = {}
    total_letters = 0

    for letter in text:

        if letter.isalpha():
            if letter not in letter_counts:
                letter_counts[letter] = 0

            letter_counts[letter] += 1
            total_letters += 1

    distribution = []

    if total_letters == 0:

        return distribution

    sorted_letters_counts = sorted(letter_counts.values(), reverse=True)

    for count in sorted_letters_counts:
        
        prob = count / total_letters
        distribution.append(prob)

    return distribution


def calculate_SSD_distance(text1, text2):

    distance = 0.0
    length = max(len(text1), len(text2))

    for i in range(length):
        
        text1_prob = 0.0
        text2_prob = 0.0

        if i < len(text1):
            text1_prob = text1[i]

        if i < len(text2):
            text2_prob = text2[i]

        prob_difference = text1_prob - text2_prob
        distance += prob_difference ** 2

    return distance

def calculate_DPD(text):

    text = text.upper()
    words = text.split()

    pattern_counts = {}

    for word in words:

        letter_counts = {}

        for letter in word:

            if letter.isalpha():
                if letter not in letter_counts:
                    letter_counts[letter] = 0

                letter_counts[letter] += 1

        sorted_counts = sorted(letter_counts.values(), reverse=True)
        pattern = tuple(sorted_counts)

        if pattern not in pattern_counts:
            pattern_counts[pattern] = 0

        pattern_counts[pattern] += 1

    distribution = {}
    total_words = len(words)

    if total_words == 0:

        return distribution

    for pattern in pattern_counts:

        distribution[pattern] = pattern_counts[pattern] / total_words

    return distribution

def calculate_DPD_distance(text1, text2):
    
    all_patterns = set(text1.keys())
    all_patterns.update(text2.keys())

    distance = 0.0

    for pattern in all_patterns:
        prob1 = text1.get(pattern, 0.0)
        prob2 = text2.get(pattern, 0.0)

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
        with open(filename, "r") as file:
            sample_text = file.read()

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
    raise NotImplementedError()

def cliSSDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """
    raise NotImplementedError()

def cliDPDTest(ciphertext_files, sampletext_files):
    """
    Args:
        ciphertext_files (list of str)
        sampletext_files (list of str)
    Returns:
        dict
    """
    raise NotImplementedError()

def generateMapping(dictionary: dict):
    """
    Args:
        dictionary (return value of cliSSDTest or cliDPDTest)
    Returns:
        A classification mapping (dict) of the ciphertexts.
        Please refer to the assignment instructions for the required format.
    """
    raise NotImplementedError()

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

if __name__ == "__main__" and not flags.interactive:
    test()