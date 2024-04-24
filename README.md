# groq-frontend
Super lightweight frontend for [the groq API](https://console.groq.com/docs/quickstart).

- Has a rudimentary memory for follow-up questions
- Customizable system prompt
- Session reset

That's about it!

![CleanShot 2024-04-24 at 09 58 00](https://github.com/dep/groq-frontend/assets/55112925/3110cf44-7180-436b-ad4c-ea97b804c71e)
_Speeds above are in realtime_

You may need these requirements:

```
pip install flask groq markdown
```

Start it up:

```
python app.py
```

This assumes you have your `GROQ_API_KEY` env var set. You can get one [here](https://console.groq.com/keys)
