# Initialize git repository

In the local project folder:

```bash
git init
git touch .gitignore
git add .
git commit -m initial-commit
```

Linux server

```bash
mkdir <PROJECT_NAME>.git
cd <PROJECT_NAME>.git
git --bare init
```

In the local project folder:

```bash
git remote add origin ssh://<SERVER_NAME>/<PATH_TO_GIT_ROOT>/<PROJECT_NAME>.git
git push --set-upstream origin master
```

Daily work in local project folder:

```bash
git status
git add .
git commit -m <COMMIT_MESSAGE>
git push
git pull
```

Work in linux console on the server:

```bash
git clone <PATH_TO_GIT_ROOT>/<PROJECT_NAME>.git
mkdir <PROJECT_NAME>
```

