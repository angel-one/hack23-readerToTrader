import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as strml
import yfinance as yfin

openai.api_key = open('/Users/akanksha.sonkar/TradeChatBot/Current/API_KEY', 'r').read()

def get_stock_price(ticker):
    return str(yfin.Ticker(ticker).history(period='1y').iloc[-1].Close)

def calculate_SMA(ticker, period):
    data = yfin.Ticker(ticker).history(period='1y').Close
    return str(data.rolling(window=period).mean().iloc[-1])

def calculate_EMA(ticker, period):
    data = yfin.Ticker(ticker).history(period='1y').Close
    return str(data.ewm(span=period, adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yfin.Ticker(ticker).history(period='1y').Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14-1,adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def plot_stock_price(ticker):
    tkr = yfin.Ticker(ticker)
    data = yfin.Ticker(ticker).history(period='1y')
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel(f'Stock Price in {tkr.info["currency"]}')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()

functions = [
    {
        'name': 'get_stock_price',
        'description': 'gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example NTPC for NTPC Ltd).'
                }  
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'calculate_SMA',
        'description': 'Calculate the simple moving average for a given stock ticker and a period.',
        'parameters': {
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example NTPC for NTPC Ltd).'
                },
                'period': {
                    'type':'integer',
                    'description':'The timeframe to consider when calculating the SMA'
                }
            },
            'required': ['ticker', 'period'],
        },
    },
    {
        'name': 'calculate_EMA',
        'description': 'Calculate the exponential moving average for a given stock ticker and a period',
        'parameters': {
            'type':'object',
            'properties': {
                'ticker': {
                    'type':'string',
                    'description':'The stock ticker symbol for a company (for example NTPC for NTPC Ltd).'
                },
                'period': {
                    'type':'integer',
                    'description':'The timeframe to consider when calculating the EMA'
                }
            },
            'required': ['ticker', 'period'],
        },
    },
    {
        'name': 'calculate_RSI',
        'description': 'Calculate the RSI for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example NTPC for NTPC Ltd).'
                }  
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_stock_price',
        'description': 'Plot the stock price for the last year given the tickersymbol of a company',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example NTPC for NTPC Ltd).'
                }  
            },
            'required': ['ticker']
        }
    },
]

# proposal remove default 1 year period and take it from func

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'plot_stock_price': plot_stock_price
}

if 'messages' not in strml.session_state:
    strml.session_state['messages'] = []

strml.title('Stock Analysis AngelOne Chatbot')

user_input = strml.text_input('Your input:')

if user_input:
    try:
        strml.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})

        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo-0613',
            messages = strml.session_state['messages'],
            functions = functions,
            function_call = 'auto'
        )

        response_message = response['choices'][0]['message']

        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])

            if function_name in ['get_stock_price', 'calculate_RSI', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            else:
                args_dict = {'ticker': function_args.get('ticker'), 'period': function_args.get('period')}

            function_to_call = available_functions[function_name] 
            function_response = function_to_call(**args_dict)   

            if function_name == 'plot_stock_price':
                strml.image('stock.png')
            else:
                strml.session_state['messages'].append(response_message) 
                strml.session_state['messages'].append(
                    {
                        'role': 'function',
                        'name': function_name,
                        'content': function_response
                    }
                )
                second_response = openai.ChatCompletion.create(
                    model = 'gpt-3.5-turbo-0613',
                    messages = strml.session_state['messages']
                )

                strml.text(second_response['choices'][0]['message']['content'])
                strml.session_state['messages'].append({'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
        else:
            strml.text(response_message['content'])
            strml.session_state['messages'].append({'role': 'assistant', 'content': response_message['content']})
    except Exception as e:
        raise e
