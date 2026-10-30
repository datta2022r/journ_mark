# Marketing Journals (PWA)

A free, serverless phone app that lists new articles (title + abstract) from top marketing journals.

## Features
- Daily auto-update of articles (GitHub Action + OpenAlex)
- Save for later (kept on your device, survives article rotation)
- Keyword filters: free-text search plus saved keyword chips you can toggle
- "New since last visit" badge and a New-only filter
- Works offline with the last downloaded list; installable to your home screen

## Set up (about 10 minutes)
1. Create a new GitHub repository and upload all these files (keep the `.github` folder).
2. Edit `MAILTO` in `fetch.py` to your email. Review the `JOURNALS` list against the ABDC list.
3. Repo Settings > Pages > Deploy from branch > `main` / root.
4. Repo Actions tab > "fetch-articles" > Run workflow (first run fills `articles.json`; it then runs daily).
5. Open `https://<your-username>.github.io/<repo-name>/` on your phone:
   - iPhone: Safari > Share > Add to Home Screen
   - Android: Chrome menu > Install app

## Run locally
    pip install requests && python fetch.py
    python -m http.server 8000     # open http://localhost:8000

## Notes
- Sample articles are replaced on the first real fetch.
- Check the journal names printed by `fetch.py`; any marked "not an exact match" should be fixed.
- Saved articles and keywords live in your browser storage; clearing site data removes them.
