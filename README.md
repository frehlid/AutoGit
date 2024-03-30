# AutoGit
A project that uses LLMs to automatically decide when to make git commits, and how to describe them. Using a small 7b parameter model, the project first asks the llm if the changes are worthy of a commit. If the model responds "yes", then we ask it to write a short commit message and push the changes!

## Getting started
To use this project, you must host the llmServer somewhere. While the model is small enough to perform decently on a CPU, it is reccomended that you host the server on a device with a dedicated GPU that has at least 8gb of VRAM. 

To automatically make commits, point the autoGit script to your server, and run it!

## TODOS:
- Prompt engineering: make the model more compliant in answering "Yes" or "No", rather than dodging the question.
- Perodically check for changes and then automatically send to the server.
