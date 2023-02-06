# telegram-payments-bot

## test startup
1. First, create python virtual environment and activate it:

```bash
python3.x -m venv env
. ./venv/bin/activate
```

2. Install all the requirements:

```bash
pip install -r requirements.txt
```

3.Start the local server for receiving incoming connections. I use ngrok for this purpose:

```bash
ngrok http 5000
```

4. Modify the .env.example with your data and save it just as ".env"
5. Run the src module:

```bash
python3 -m
```

