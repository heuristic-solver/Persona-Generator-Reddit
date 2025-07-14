import requests
import re
import sys
import google.generativeai as genai
import json


url = input("Enter URL: ").strip()


match = re.match(r"https?://(www\.)?reddit\.com/user/([^/]+)/?", url)
if not match:
    print("Invalid Reddit user URL.")
    sys.exit(1)
username = match.group(2)
print(f"Fetching data for u/{username}...")


data_kind = "comments"
url_comments = f"https://www.reddit.com/user/{username}/{data_kind}.json"
headers = {"User-Agent": "RedditPersonaBot/0.1"}
params = {"limit": 100}
comments = []
after = None
while len(comments) < 100:
    if after:
        params["after"] = after
    resp = requests.get(url_comments, headers=headers, params=params)
    if resp.status_code != 200:
        break
    data = resp.json()
    children = data.get("data", {}).get("children", [])
    if not children:
        break
    comments.extend(children)
    after = data.get("data", {}).get("after")
    if not after:
        break
comments = comments[:100]


posts = []
data_kind = "submitted"
url_posts = f"https://www.reddit.com/user/{username}/{data_kind}.json"
after = None
while len(posts) < 100:
    if after:
        params["after"] = after
    resp = requests.get(url_posts, headers=headers, params=params)
    if resp.status_code != 200:
        break
    data = resp.json()
    children = data.get("data", {}).get("children", [])
    if not children:
        break
    posts.extend(children)
    after = data.get("data", {}).get("after")
    if not after:
        break
posts = posts[:100]


texts = []
for c in comments:
    body = c["data"].get("body", "")
    if body:
        texts.append(body)
for p in posts:
    selftext = p["data"].get("selftext", "")
    title = p["data"].get("title", "")
    if title:
        texts.append(title)
    if selftext:
        texts.append(selftext)
all_text = "\n".join(texts)
user_text = all_text[:4000]


genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("models/gemini-1.5-flash")
prompt = (
    "Given the following Reddit posts and comments by a user, analyze and infer a detailed persona. "
    "Return your answer as a JSON object with the following fields: "
    "'summary' (a 2-3 paragraph persona summary), 'interests' (list), 'writing_style' (string), 'self_disclosed_info' (string), 'tone' (string), and 'activity' (string). "
    "Posts and comments:\n"
    f"{user_text}\n"
    "Persona (JSON):"
)
response = model.generate_content(prompt)

try:
    persona_json = json.loads(response.text)
except Exception:
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        persona_json = json.loads(match.group(0))
    else:
        persona_json = {"summary": response.text.strip()}

fname = f"persona_{username}.txt"
with open(fname, "w", encoding="utf-8") as f:
    f.write(f"User Persona for u/{username}\n\n")
    f.write(persona_json.get("summary", "") + "\n\n")
    f.write("Structured Persona Fields:\n")
    for key in ["interests", "writing_style", "self_disclosed_info", "tone", "activity"]:
        value = persona_json.get(key, "")
        f.write(f"- {key}: {value}\n")
print(f"Persona written to {fname}")