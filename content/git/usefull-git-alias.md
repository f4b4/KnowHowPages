# Usefull git alias

## Add, Commit and Push in one command
```ini
   [alias]
     acp = "!f() { msg=\"$1\"; shift; git add -A && git commit -m \"$msg\" \"$@\" && git push; }; f"
```
```bash
git acb '{COMMIT_MSG}'
```