# nudge-jar

`nudge-jar` is a tiny Flask app for saving short prompts to your future self and pulling one at random when you need momentum.

## What the app does

- Shows a single-page interface at `/`
- Loads the current in-memory nudge list from the API
- Saves new nudges with `POST /api/nudges`
- Picks one saved nudge at random with `GET /api/nudges/random`
- Keeps all data in memory, so restarting the app clears the jar

## Project structure

```text
nudge-jar/
  app.py
  requirements.txt
  Dockerfile
  .dockerignore
  README.md
  templates/
    index.html
  static/
    style.css
  tests/
    test_app.py
```

## Requirements

- Python 3.12+ recommended
- `pip` for installing dependencies

## Run locally

Install dependencies and start the app:

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

Optional debug mode:

```bash
FLASK_DEBUG=1 python app.py
```

Windows PowerShell:

```powershell
$env:FLASK_DEBUG = "1"
python app.py
```

## API behavior

### `GET /`

Returns the HTML page for the nudge jar UI.

### `GET /api/nudges`

Returns the full list of saved nudges:

```json
{
  "nudges": ["Send the email", "Drink water"]
}
```

### `POST /api/nudges`

Accepts JSON in this shape:

```json
{
  "text": "Send the email"
}
```

Successful response:

```json
{
  "ok": true,
  "nudges": ["Send the email"]
}
```

If the text is empty or only whitespace, the app returns:

```json
{
  "error": "Nudge cannot be empty."
}
```

with HTTP `400`.

### `GET /api/nudges/random`

Returns one randomly selected nudge:

```json
{
  "nudge": "Drink water"
}
```

If no nudges have been saved yet, the app returns:

```json
{
  "error": "Add a nudge first."
}
```

with HTTP `404`.

## How the page works

1. Opening `/` loads the HTML interface.
2. The page fetches `GET /api/nudges` and renders the current list.
3. Submitting the form sends `POST /api/nudges` with JSON.
4. Clicking `Pick One` requests `GET /api/nudges/random`.
5. The page updates in place without a full reload.

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- page rendering
- empty-state API behavior
- nudge creation and whitespace trimming
- random selection behavior

## Docker

Build and run the container:

```bash
docker build -t nudge-jar .
docker run -p 5000:5000 nudge-jar
```

Then open `http://127.0.0.1:5000`.

## Notes

- Data is stored only in memory.
- Restarting the server clears all saved nudges.
- This project is intentionally small and learning-focused.
