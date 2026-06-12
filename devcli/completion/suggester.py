from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
import os
import difflib

class DevAutoSuggest(AutoSuggest):

    def get_suggestion(self, buffer, document):
        text = document.text

        if not text.strip():
            return None

        words = text.split()

        # 🔥 1. MULTI-COMMAND MEMORY (best match, most recent first)
        history = list(buffer.history.get_strings())
        history.reverse()

        scored = []
        for entry in history:
            if entry.startswith(text):
                # Higher score = better match (longer prefix match)
                score = len(text) / len(entry)
                scored.append((score, entry))

        if scored:
            scored.sort(reverse=True)
            best = scored[0][1]
            return Suggestion(best[len(text):])

        # 🔥 2. PATH SUGGESTION (for cd, type, etc.)
        if words[0] in ["cd", "type", "dir", "ls"]:
            partial = words[-1]

            base = os.path.dirname(partial) if os.path.dirname(partial) else "."
            prefix = os.path.basename(partial)

            try:
                items = os.listdir(base)
            except Exception:
                items = []

            # Match paths
            matches = [i for i in items if i.lower().startswith(prefix.lower())]

            # Fallback fuzzy
            if not matches and prefix:
                matches = difflib.get_close_matches(prefix, items, n=3, cutoff=0.3)

            if matches:
                match = matches[0]

                # Add slash if directory
                full_path = os.path.join(base, match)
                if os.path.isdir(full_path):
                    match += os.sep

                return Suggestion(match[len(prefix):])

        # 🔥 3. BASIC COMMAND MEMORY (fallback)
        for entry in history:
            if entry.startswith(text):
                return Suggestion(entry[len(text):])

        return None