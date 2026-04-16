# nudge-jar

A tiny Flask app for saving short nudges to your future self and pulling one at random when you need momentum.

## Idea

Add one-line prompts like "Send the email" or "Drink water," then click **Pick One** to surface a random nudge.

## Structure

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

## Data flow

1. `GET /` returns the page.
2. The page loads nudges from `GET /api/nudges`.
3. Saving a nudge sends `POST /api/nudges` with JSON.
4. Clicking **Pick One** calls `GET /api/nudges/random`.
5. Flask reads or updates the in-memory list and returns JSON.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

Optional development mode:

```bash
FLASK_DEBUG=1 python app.py
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Docker

```bash
docker build -t nudge-jar .
docker run -p 5000:5000 nudge-jar
```

## Notes

- Data is stored only in memory.
- Restarting the server clears the jar.
- This project is intentionally small and learning-focused.
