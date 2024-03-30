from llama_cpp import Llama
from flask import Flask, request, jsonify

llm = Llama(
  model_path="./mistral-7b-instruct-v0.2.Q4_K_M.gguf",  
  #n_ctx=32768,  
  n_threads=8,            
  chat_formaat="llama-2"
  #n_gpu_layers=35         
)
def ask_should_commit(changes):
    response = llm.create_chat_completion(
            messages = [
                {"role": "system", 
                 "content": "You are a git assistant. You can only answer with one word, 'yes' or 'no'. Do not explain your answer more."},
                {"role": "user",
                 "content": f"Are these git changes worth committing to git? {changes}. You must answer with one word, 'yes' or 'no'. Do not explain your answer more."
                 }
            ])
    return response['choices'][0]['message']['content']

def ask_commit_message(changes):
    response = llm.create_chat_completion(
            messages = [
                {"role": "system", 
                 "content": "You are a git assistant. You only respond with messages for git commits."},
                {"role": "user",
                 "content": f"What message would you write for this git commit? {changes} Only respond with the commit message."
                 }
            ])
    return response['choices'][0]['message']['content']

def ask_commit():
    should_commit = ""
    first_word = ""
    while True:
        should_commit = ask_should_commit(changes)
        print(should_commit)
        first_word = should_commit.split()[0]
        print(first_word)
        if (first_word == "Yes" or first_word == "No" or first_word == "Yes." or first_word == "No."):
            break

    if (first_word == "No"):
        return ""

    return ask_commit_message(changes)

app = Flask(__name__)

@app.route("/getCommit", methods=['POST'])
def get_commit():
    data = request.json
    input_changes = data.get("changes", "")
    commit_message = ask_commit(input_changes)

    if (commit_messae == ""):
        return jsonify({"should_commit": "No", "message":"Changes are not deemed significant enough for a commit"})
    else:
        return jsonify({"should_commit":"Yes", "message":commit_message})


