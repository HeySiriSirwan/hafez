# Daily Hafez Poem

This project is a personal work, started just out of curiosity and for coding practice—nothing serious or professional.  
I used Python to build a simple tool for working with Hafez's poems. There’s no big claim or goal here; I just did it for fun and learning.

Some parts of the project may be incomplete or basic, as my main intention was to enjoy the process and improve my skills. If anyone finds it useful or wants to improve it, that would make me happy.

## Features

- Access to Hafez's poems
- Get a random poem/verse
- Send poems to Twitter automatically  
(Some features might still be incomplete or added later.)

## Installation

Clone the repository:

```bash
git clone https://github.com/HeySiriSirwan/hafez.git
cd hafez
```

(Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can run the main script:

```bash
python main.py
```

This will select a random poem (or verse) from Hafez and send it to Twitter (if API keys are configured).

## Project Structure

```
hafez/
│
├── .github/workflows/flow.yml   # GitHub Actions workflow for scheduled posting
├── poetry_handler.py            # Handles loading and selecting poems
├── main.py                      # Main entry point for running the project (builds message and posts to Twitter)
├── config.py                    # Handles environment configuration
├── utils.py                     # Utility functions
├── hafez_ghazals.json           # Poems dataset
├── requirements.txt             # dependencies
└── README.md
```

## Contributing

If anyone wants to contribute, feel free. I’d be glad if this project is useful for someone else.

---

This is a personal and experimental project, made just for practice and fun.
