import ollama
import re
import logging

logger = logging.getLogger(__name__)

class OllamaHealer:
    def __init__(self, model="qwen2.5-coder:7b"):
        self.model = model

    def get_healed_locator(self, failed_locator, page_source, element_description):
        # We clean the HTML to save tokens (remove scripts/styles)
        clean_html = re.sub(
            r"<(script|style).*?>.*?</\1>", "", page_source, flags=re.DOTALL
        )

        prompt = f"""
        You are a Selenium Expert. A test failed because the locator '{failed_locator}' was not found.
        The element is described as: '{element_description}'.
        
        Analyze this HTML snippet and find the most likely new XPath for this element:
        {clean_html[:15000]}  # Truncate to stay within context limits

        Rules for XPath Generation:
            1. Use 'normalize-space()' for all text comparisons to handle hidden spaces and newlines. 
               Example: //button[contains(normalize-space(), 'Login')]
            2. Avoid using exact text matches like text()='Value'.
            3. If the element has a stable attribute like @type or @name, combine it with the text.
            4. DO NOT use backticks, quotes, or markdown code blocks.
            5. Return ONLY the XPath string. No backticks. No explanations.
        """

        response = ollama.generate(model=self.model, prompt=prompt)
        raw_xpath = response["response"].strip()
        logger.info(f"Ollama raw XPath response: {raw_xpath}")
        return raw_xpath

        """
        # SANITIZATION STEP:
        # Remove markdown code blocks (```xpath ... ```)
        clean_xpath = re.sub(r"```[a-z]*\n?", "", raw_xpath)
        # Remove all backticks, quotes, and newlines
        clean_xpath = (
            clean_xpath.replace("`", "")
            .replace('"', "")
            .replace("'", "")
            .replace("\n", "")
            .strip()
        )
        """
        #logger.info(f"Ollama cleaned XPath: {clean_xpath}")
        
