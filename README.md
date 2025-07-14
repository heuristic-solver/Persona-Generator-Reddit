# Persona-Generator-Reddit
This Python script scrapes a Reddit user's posts and comments and builds a basic persona profile showing things like interests and their most active time.

# Instructions 
1. Clone the repo
   ```bash
   git clone https://github.com/heuristic-solver/Persona-Generator-Reddit
   ```
2. Install requirements.txt
   ```bash
   python -r requirements.txt
   ```

3. Gemini API Key
   You can get your api key from https://aistudio.google.com/apikey
5. Run the code
   ```bash
   python reddit_persona.py
   ```



# Note 
- This uses the reddit public api so no specific api key is needed. It is also limited to 100 comments per user and the analysis is a simple LLM based one. 
- If you experience any dependancy issue (Example: Numpy version issues) create a venv 

