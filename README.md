CS73-Word-Salad
===============
EDIT DISTANCE
gen_dictionaries.py contains code for creating phon_pickle.txt and layer_pickle.txt, which are representations of dictionaries made from CMU_dict.txt, the CMU phonetic dictionary, and phoneme_output.txt, which is used to create fsts for Carmel. It can be run from the command line as:

python gen_dictionaries.py CMU_dict.txt

These two output files are necessary to run edit_dist_generator.py, which is a version of the game that can be run from terminal with the following command:

python edit_dist_generator.py phonemes_confusion.txt phon_pickle.txt layer_pickle.txt

The order of the arguments matters.

CARMEL
gen_fsts.py is a file that takes the CMU dictionary and formats the four required transducers into text files formatted for use with Carmel. It can be run from the command line as:

python gen_fsts.py phoneme_output.txt

After which the four output files can be put through Carmel on the tahoe server using the following command:

$ cat input.noe | carmel -qbsriWIEk 1 gen_words.fsa words_phonemes.fst phonemes_phonemes.fst phonemes_phonemes.fst > results.txt

WEB INTERFACE
The CGI files are provided for reference. The web version of the game can be accessed at http://tinyurl.com/wordsaladgame. This version can take any number of inputs, however 3-4 is recommended.
