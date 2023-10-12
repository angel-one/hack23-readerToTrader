
# Stock Analysis AngelOne Chatbot with ChatGPT in Python

## Overview:
This Python-based chatbot uses OpenAI's ChatGPT to provide answers to frequently asked questions (FAQs) related to the stock market. It can answer queries about the current stock price of a particular stock, SMA, EMA, RSI and even generate the plots for stock’s historical price data. We obtain live stock data using Yahoo Finance API (yfinance). It dynamically handles responses, invoking appropriate functions based on user queries and presenting the results in a user-friendly manner.

### Abbreviations
SMA - Simple Moving Average<br>
EMA - Exponential Moving Average<br>
RSI - Relative Strength Index<br>

## Prerequisites:
Python 3.6 or later<br>
OpenAI GPT-3.5 API key (you can sign up for access on the OpenAI website)<br>
### Required Python libraries (install using pip):
openai<br>
pandas<br>
matplotlib<br>
yfinance<br>
streamlit<br>

## Installation:
### Clone this repository into your local machine:

```shell
git clone git@github.com:angel-one/hack23-readerToTrader.git
```

### Install required python packages:
```shell
pip install pandas openai matplotlib yfinance streamlit
```

### Create a .env file in the project directory to store your OpenAI GPT-3.5 API key. 
```shell
OPENAI_API_KEY=your-api-key-here
```

### Working demo of AngelOne Chatbot
https://drive.google.com/drive/u/0/folders/15VNgf0RJYtQF5LGNYDxY55BKUl7-_Au4
