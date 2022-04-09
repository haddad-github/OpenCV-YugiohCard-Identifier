# Yugioh Card Identifier
 ## Summary
 Given the image of a yugioh card deck, the cards in this deck will be found and identified using object-detection with OpenCV
 
 Each yugioh card will be loaded, resized and then template-matched using the TM_COEFF_NORMED method
 ![image](https://user-images.githubusercontent.com/68672661/162574585-426aad0e-60b6-409f-bfd0-a361a6849217.png)
##### Documentation: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html

## Usage
There's the main.py file that is the commandline version of the script; all values have to be changed manually in the code itself.

There's the primary version which is the mainWithGUI.py file, that is the GUI version of the script.

Typical usage, in order:
![explain2](https://user-images.githubusercontent.com/68672661/162575006-48317c8f-de32-444a-99e0-30053a5a8b68.jpg)
1) Click "Browse" and locate your deck's image file and then click "Load deck"; it'll show you a preview of the deck you loaded in a 300x300 format
2) Choose the card dimensions theh press "Confirm dimensions". You have to use some software or open it on Paint and drag across a card to get the width x height of a card on your image, as shown below. Default values (by entering 0) are for Master Duel (1920x1080), which has a format is 64x94.
![explain1](https://user-images.githubusercontent.com/68672661/162575085-b3c2f393-276f-4407-8a74-335a50783c88.jpg)
3) Choose the accuracy coefficient then press "Confirm coeff". For cleaner formats (that don't have special tags that obstruct the card's image like in Master Duels), you can use something around 0.80 for better chances at getting the full list of cards. The higher you go, the more certainty is required to pass that threshold and so you'll end up with less cards being identified. For Master Duel format, I would advise something around 0.62 - 0.70, the reason being that Master Duel decks have the "N/R/SR/UR" tags on the cards, which throws off object detection to some significant extent, so you'll need to compensating by reducing the accuracy coefficient threshold.
4) Click "Identify cards" to activate card detection. Waiting time using 20 threadpool is around 3 minutes for me (i7 8700k @ 3.2Ghz/16GB 3200Mhz). You may experience some lag based on your system. If so, you can change the number "20", in line 57 (threadedMatch() function) of main.py, to something smaller. This will increase your time of execution.
5) After the card identification is done, the right side of the GUI will have a dropdown of all the identified cards. You will be able to pick a card and display it in full-size.

Here's another image, this time with a Master Duel format (notice the 0.67 accuracy coefficient used as opposed to the previous picture).
![explain3](https://user-images.githubusercontent.com/68672661/162575502-30bd21a5-55e0-4fbb-9b6c-01b58c412b7c.jpg)

## Limitations and improvements to be made
1) Currently, the user must determine the size of the card on his deck image in order for the script to resize the card images to match those dimensions. I hope to automatically detect a card and extract its dimensions automatically.
2) Currently, the accuracy for Master Duel format is not ideal, some mistakes are expected and some cards are missed because of the rarity tags (N/R/SR/UR) superimposed on the card images. I hope that I will able to apply those tags to the card images being loaded in, as to make them identitical to the Master Duel format and increase the accuracy drastically.
3) Currently, although the script is functional, the speed and the ressources used for the script are in drastic need of improvement. I hope that I will be able to switch over to a faster matching method (*potential drawback: less accurate*) and will not have to use multithreading to give it a reasonable execution time. Some methods may be histogram comparisons, nearest-neighbors based on certain color schemes, and a mix of those perhaps.
