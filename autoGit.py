import subprocess
import requests
import json

server_address = "http://127.0.0.1:5000"
headers = {
    'Content-Type': 'application/json'
}

def get_current_changes():
    try:
       # print("ran git add .")
        changes = subprocess.run(['git', 'diff'], capture_output=True, text=True, check=True)
        if (changes.stdout):
            changes = changes.stdout
        else:
            changes = ""
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    return changes

def git_push(commit_message):
    try:
        subprocess.run(['git', 'add', '.'])
        subprocess.check_call(['git', 'commit', '-m', commit_message])
        subprocess.check_call(['git', 'push'])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")


def get_commit_message():
    changes = get_current_changes()
    if (changes == ""):
        return ""
   # print(changes)
    
    r = requests.post(f"{server_address}/getCommit", json={"changes": changes}, headers=headers)
    print(r.text)

    r = json.loads(r.text)

    if (r.get("should_commit")  == "Yes"):
        message = r.get("message").replace("Commit message:", "")
        git_push(message)

if  __name__ == "__main__":
    get_commit_message()



