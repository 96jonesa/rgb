# rgb

This repo contains the processing code used in a Reddit bot which replies to new submissions and comments, correcting who to whom where appropriate just as its namesake from the TV show Friends would. It can process every new submission and comment on all of Reddit in real-time using only a single CPU core. The name username is obscured to prevent random people from searching for this code for the sake of spawning clones. The username is the character's first name, then last name, then Bot, with no spaces.

In order to prevent clones from popping up, the code here is slightly modified and the Reddit interaction is removed - please do not spawn clones: they will cost you money to run, they will be a nuisance to the Reddit community, they will ruin the joke, and you will be like, totally lame if you do. Seriously, like sooo lame.

# How it works

The text being processed is run through a dependency parser and a named entity recognizer. If any token cast to lowercase is equal to 'who', is considered the object of a verb according to the dependency parser, and is not considered part of a named entity according to the named entity recognizer, then it is corrected to the appropriately capitalized 'whom'. The phrase used in the correction will be the span from the 'whom' to the root verb, or vice versa depending on the ordering. The 'whom' is surrounded by asterisks, which italicizes it on Reddit. Several explicit omission rules are used to prevent incorrect corrections - the priority is to rarely if ever make incorrect corrections, and in the presence of atrocious grammar and spelling there are certain patterns which almost always confuse the dependency parser and/or the named entity recognizer. The live version of the bot includes additional explicit omission rules not included here.

Basically:

1. Find 'who'
2. Check if object of verb and thus should be changed
3. Check if part of name and thus should not be changed
4. Check for exceptions
5. Correct to 'whom'

# Use via Colab

Before bothering to install dependencies: if you only want to tinker with the code as a demo, then the Colab notebook version will suffice and save you some time and resources.

Navigate to the rgb.ipynb file in this repo. At the top of the file, you will see an 'Open in Colab' button. Click it.

You may need to log in to a Google Drive account to proceed.

Modify the text_list variable at the top of the file to contain whatever list of texts you wish to process, or just use the default texts.

Run it by pressing Ctrl+F9 (or Cmd+F9), by navigating to Runtime > Run all, or by running each cell individually in order.

# Installation

Download the rgb.py file from this repo.

You will need to have Python version 3.6 or later, as well as pip3 to install dependencies.

You will need to have PyTorch version 1.1.0 or later. Check https://pytorch.org/get-started/locally/ for installation instructions.

If you are using Windows and experience an error in the pip3 installation of PyTorch, try the tip from https://docs.python.org/3.7/using/windows.html section 3.1.2.

You will need to install spaCy and flair:

    pip3 install spacy
    pip3 install flair
    
You will need to download the spaCy language model separately:

    python3 -m spacy download en_core_web_sm
    
# How to use

Modify the text_list variable at the top of the file to contain whatever list of texts you wish to process, or just use the default texts.

Run it:

    python3 rgb.py

The first time you run it, it will automatically download the named entity recognizer for flair. It is 432 MB, so this may take a while.

# Shout out to the guy who had the idea

A few days ago my buddy called me up and said "Andy you know how in the show Friends Ross is always correcting people when they say who instead of whom? You should make a Reddit bot that does that!"

So I did.

https://github.com/hailrobotoverlords AKA Gary from the Garage
