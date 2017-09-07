# Overview
Deep learning RNN trained on NOAA hurricane / tropical storm advisories. Several hundred storm forecasts were downloaded from the NOAA archives for 2006-2016 at http://ftp.nhc.noaa.gov/atcf/archive/

Included is a notebook for downloading the advisories saved into a single adv.txt file (included). The second notebook contains the RNN code which trains a 45 character RNN using a 3 layer LSTM RNN. You can experiment with different character lengths, batch sizes, designs, etc. Wasn't too concerned about overfitting since most of the focus was on creating something that looked reasonably legimitate.

Project adapted from Udacity's intro to RNN's notebook. I added some flexibility to tweak paramaters via function calls

https://github.com/udacity/deep-learning/blob/master/intro-to-rnns/Anna_KaRNNa.ipynb