# TGAnalyzingBot

This bot can get read messages from specified news channels, store them and classify.

Current classes:
  * Software
  * Device
  * Other  
  * Ads
  * Research
  
  
## Installation

You should have ***python3.9*** !

### 1. Loading data from GitHub

```
  git clone https://github.com/matweykai/TGAnalyzingBot.git
 
  # Changing current directory to 'TGAnalyzingBot'

  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt  
```

### 2. Configurating bot

You should create directory for log files (Default: logs):
```
  TGAnalyzingBot
  ├───logs  # Maybe another name
```
Than you should configure '.env_template' file:
```
  API_ID=...
  API_HASH=...
  DB_STR=...(sqlite:///bot_base.db)
  MODEL_PATH=...(default: classification_model.mdl)
  LBL_ENC_PATH=...(default: label_encoder.obj)
  LOGGING_PATH=...(default: logs)
```

Than you should change it name to '.env'

So result structure:
```
  TGAnalyzingBot
  ├───logs  # Maybe another name
  ├───.env
```

## Usage

You should change your directory to ***TGAnalyzingBot/code*** and run ***main.py*** file:
```
  python main.py <parameters>
```

Parameters:

> * -a \<channel name\> &emsp;# Bot reads first 300 messages and subscribes this channel
> * -u&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;# Bot loads unread messages from all added channels