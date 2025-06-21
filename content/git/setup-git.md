---
layout: post
---

In the local project folder:

{% highlight bash %}
git init
git touch .gitignore
git add .
git commit -m initial-commit
{% endhighlight %}

Linux server

{% highlight bash %}
mkdir <PROJECT_NAME>.git
cd <PROJECT_NAME>.git
git --bare init
{% endhighlight %}

In the local project folder:

{% highlight bash %}
git remote add origin ssh://<SERVER_NAME>/<PATH_TO_GIT_ROOT>/<PROJECT_NAME>.git
git push --set-upstream origin master
{% endhighlight %}

Daily work in local project folder:

{% highlight bash %}
git status
git add .
git commit -m <COMMIT_MESSAGE>
git push
git pull
{% endhighlight %}

Work in linux console on the server:

{% highlight bash %}
git clone <PATH_TO_GIT_ROOT>/<PROJECT_NAME>.git
mkdir <PROJECT_NAME>
{% endhighlight %}

