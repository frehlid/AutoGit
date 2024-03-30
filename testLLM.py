from llama_cpp import Llama

llm = Llama(
  model_path="./mistral-7b-instruct-v0.2.Q4_K_M.gguf",  
  #n_ctx=32768,  
  n_threads=8,            
  chat_formaat="llama-2"
  #n_gpu_layers=35         
)
changes = """ diff --git a/test_calculator.py b/test_calculator.py
index 1deadbeef..feebdaed 100644
--- a/test_calculator.py
+++ b/test_calculator.py
@@ -4,5 +4,10 @@ from calculator import add, subtract, multiply
 def test_add():
     assert add(2, 3) == 5
 
 def test_subtract():
     assert subtract(5, 2) == 3
 
 def test_multiply():
     assert multiply(3, 4) == 12
 
+def test_divide():
+    assert divide(10, 2) == 5
+    assert divide(5, 2) == 2.5
"""

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
        return

    return ask_commit_message(changes)

print(ask_commit())

            

# Simple inference example
#output = llm(
#+ \n Is this enough change to warrant a git commit? Yes or no:""",
#  max_tokens=512,  # Generate up to 512 tokens
#  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
#  echo=True        # Whether to echo the prompt
#)
#print(output)

# Chat Completion API
