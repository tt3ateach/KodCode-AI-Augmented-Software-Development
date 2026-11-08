# Demo 3 · prompt

Copilot Chat in **Agent** mode, a model that accepts images (Auto is fine; check in rehearsal), an empty folder
open in VS Code. Attach your own photographed sketch, or `feedback_sketch.png`, then paste:

```
Build the page in the attached sketch as one self-contained index.html (HTML, CSS and JavaScript, no
libraries). Follow the layout and the notes in red. Serve the folder with python -m http.server 8000, open
http://localhost:8000 in the integrated browser, take a screenshot, compare it with the sketch, and fix any
differences. Then check in the browser that Send stays disabled until a star rating and a topic are chosen.
Finish with a short list of what you checked.
```

Afterwards, check it yourself: no stars, so Send is off; add stars and a topic, and it turns on. Then ask the
class what the agent didn't check (keyboard use, the 500-character limit, what happens on Send).
