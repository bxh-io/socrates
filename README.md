# A silly little one liner for asking questions about a URL

If you put a URL in, it will return 3 questions you can ask your report about when you want them to read an article about

```bash
OPENAI_API_KEY="YOUR_KEY" python socrates.py "URL HERE"
```

Needs this run once:

`python -m pip install openai requests beautifulsoup4`
