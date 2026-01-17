import json
import os

class LocatorStore:
    def __init__(self, filepath="testdata/healed_locators.json"):
        self.filepath = filepath
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def get_fix(self, broken_value):
        """Returns the healed locator if it exists, else None."""
        return self.cache.get(broken_value)

    def save_fix(self, broken_value, new_xpath):
        """Updates the cache and persists it to disk."""
        self.cache[broken_value] = new_xpath
        with open(self.filepath, 'w') as f:
            json.dump(self.cache, f, indent=4)