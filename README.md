# WeatherWise
_By Prakamya Singh, Praneeth Suresh, Pratyush Bansal and Ninad Dixit_

[![Watch the video](https://github.com/Praneeth-Suresh/ForecastingFastestCoderFirst/blob/main/Analysis/API_vs_AI_comparison.png)](https://github.com/Praneeth-Suresh/ForecastingFastestCoderFirst/blob/main/Analysis/WeatherWise%20demo.mp4)

## About our tool
Our tool allows the user to provide the name of a city as a command-line argument, and outputs an interactive pop-up window where the user can look at the day's weather forecast for that city. The tool uses an API key to extract data from the World Weather API service.

Additionally, our tool employs a complex AI model which uses past weather datasets to accurately predict the weather for a limited number of major cities around the globe. This AI model is cross-verified with the data received from the World Weather API service, thus improving the accuracy of the weather forecast.

## Code architecture
The user will run `frontend.py` on the command-line interface of their choice, along with 1 additional command-line argument: the name of the city for which they wish to know the weather forecast. An example is shown below:

**Windows**
```
py frontend.py london
```

**Linux/MacOS**
```
python3 frontend.py london
```

This format even works for cities with multiple words in their names:
```
py frontend.py new york
```

The user will see an pop-up window with the relevant weather info, including the following factors:
 * Single-word description of the weather
 * Actual temperature
 * Apparent temperature
 * Wind speed
 * Rainfall in the hour
 * Humidity
 * Visibility
 * Pressure
 * Cloud cover

The user can also navigate between pages on the pop-up; each page shows the forecast for a particular hour in the day, and all 24 hours in the day are covered by our tool.

For certain major cities, the user will also see an adjacent window with the prediction results from our AI model, positioned to the right of the results from the API. These results are often equally accurate in comparison to the "official" data from the API, with a 80-90% margin of accuracy (i.e. our values rarely deviate more than 10-20% from the "official" values). Our model provides values for all the above-mentioned datapoints except visibility and apparent temperature.

The flowchart [here](https://cdn.discordapp.com/attachments/1117454328836399147/1122134859683471410/image.png) will provide an overview of our architecture.

## Use of Github Copilot
Our team used Github Copilot extensively while working on the project, which greatly increased our productivity and improved our knowledge of python coding.

Due to its ability to autocomplete basic, boilerplate code, we were able to save much time on mundane aspects of the code. Basic functions, loops and conditional statements could be autcompleted using this tool, which allowed more time for us to focus on the logic of our code. Additionally, use of Github copilot reduced the number of syntax errors and hence, allowed us to better test and run our code. While we would otherwise waste time on pinpointing syntax errors, we were now able to troubleshoot the logic errors more precisely.

Due to it being an AI model, Github Copilot often gave us unique and inventive solutions for problems we faced while coding. Since Copilot is fueled by programs written by expert programmers around the world, these suggestions were often simpler to implement and less prone to errors, than our own code. Hence, Github Copilot served as our mentor by giving us useful suggestions almost instantly.

In `APIGen.py`, we wrote a code to retrieve the meteorological data from the API. However, the JSON response provided, although very detailed, was also very convoluted and difficult to clean up. Luckily, once Github Copilot had read through the JSON response output in the terminal, and once we had provided it with the list of relevant datapoints in the form of a code comment, it was able to automatically generate the code to retrieve the relevant data from the convoluted nested lists and dictionaries. It was similarly helpful during the code-writing process when we were retrieving the historical data for training our AI model(through the API once again; in the file `DatasetGenerator.py`).

We additionally combined the power of ChatGPT with Github Copilot when it came to writing the code to develop the pop-up window GUI using Python's Tkinter library. While ChatGPT allowed us to learn the basic coding constructs quickly, Github Copilot allowed us to quickly write the lines of code necessary to build, format and style the GUI while incorporating the data retrieved through our API call as well as the AI model's output. All this work was done inside of `frontend.py`.

## Comparing the AI Model to the API
Our team has added an additional feature to check the accuracy of the data by adding an AI model forecast, using huge amounts of historical data of 26 major cities in the world. This is seen as the right-hand panel in the forcast outputs for supported cities. The AI model learns on a time-series basis, and predicts output based on the most recent readings provided by us and has provided some very accurate results to the forecasted weather from the API. One limitation that we are currently working on is the increasing the training the data to include AI predictions on an hourly basis rather than every 3 hours.

We built our AI model using Tensorflow and trained it using past data from the World Weather API (`train.py`). Here too Github Copilot proved a class of its own in helping us build the Keras Sequential model that lay behind the success of the AI model. During training the loss of the model was plotted to record how well our model was doing in terms of accuracy. The following graphs show how the model started performing better as we progressed into the training process. 

<img align="left" width="100" height="100" src="https://github.com/Praneeth-Suresh/ForecastingFastestCoderFirst/blob/main/Analysis/loss_50_epochs.png">
<img align="right" width="100" height="100" src="https://github.com/Praneeth-Suresh/ForecastingFastestCoderFirst/blob/main/Analysis/loss_5_epochs.png">
