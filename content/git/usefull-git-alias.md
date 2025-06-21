# Usefull git alias

## Add, Commit and Push in one command

Add this to your global ~/.gitconfig (or run the second command to append it automatically):
```ini
[alias]
  acp = "!f() { msg=\"$1\"; shift; git add -A && git commit -m \"$msg\" \"$@\" && git push; }; f"
```

Sample call:
```bash
git acb '{COMMIT_MSG}'
```