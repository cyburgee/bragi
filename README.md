# Bragi
#### Norse God of poetry, music, and the harp.

### Requirements
I've developed and run this on my Mac with Python 3.9.6. YMMV.

The synthesizer is controlled by your computer keyboard with the pynput package. You'll probably need to run as root or give your OS permissions to read your input device.

### Setup
Clone the repo:

```git clone https://github.com/cyburgee/bragi.git```

Get in the project directory:

```cd bragi```

Setup a python [virtual environment](https://docs.python.org/3/library/venv.html):

```python -m virtualenv venv```

Activate the virtual environment:

Mac and Linux:
```source ./venv/bin/activate```

I don't know how to do this on Windows

Install dependencies:

```pip install -r requirements.txt```

### Run
Launch it!

```python -m synth```

You can play now by hitting some letter keys on your keyboard. Start with the volume turned low on your system and slowly adjust it while holding a note.

To quit just hit `Esc`

Happy playing!