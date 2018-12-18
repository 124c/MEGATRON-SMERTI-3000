# MEGATRON-SMERTI-3000
My project assignment for IT Finance course at HSE Financial Markets and Institutions programme

This project is a simulation of a trading algorithm with two basic trading indicators and a filter for them
This part is mandatory as a description of a script for assignment so you can feel free to explore it if you feel
comfortable with python


Before we start, I stroungly suggest using pycharm to be able to inspect the code 
So, first, you should run a deploy.py script 
And set a working directory to the file where the whole project is contained

More than that, you should download all the required libraries. All of them are specified in requirements.txt
packages are loaded by opening a terminal and writing there pip install -r requirements.txt 
(or you need to provide the path to requirements.txt)

Now, let's look at the deploy code
First we just load all the datasets until line 9 and set time period for our alpha tuning
Later, we load dataset with ohlc data, check if data has any NA values in it
We set a dictionary that stores parameters for alpha inside of it and initialize them randomly
Then we deploy our alpha module and generate trading signals for it. 
All outputs are stored in the datasets folder, all in sub-folders according to the module name
Alpha engine generates values for rsi, macd, hurst, all with the parameters from the dict, and stores the dataframe
After that, we pass these values back to backtesting engine, where we calculate pnl, confusion matrix and calculate the ratio
of right/wrong predictions. All that is saved back to it's folder
Next we deploy a part of our visualization module, which showc cummulative return with random variables
Now this is the time where we start optimization engine, which calculates all possible outputs, clusters them and chooses
the cluster index for the centroid with the highest return. This helps us avoid non-robust regions while tuning the model
All of these heatmaps are plotted automatically by one of our modules
After that we save the dictionary in 'pickle' extension and the load it back on the next lines

Finally we test that parameters with the new data and see how our returns look like on web page
