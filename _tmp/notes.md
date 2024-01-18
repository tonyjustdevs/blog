1. create any local folder and open terminal and run:
git clone https://github.com/tonyjustdevs/tonyjustdevs.github.io.git

2. open the cloned folder as root - this goes to 'main' branch:
cd <cloned_repository_folder> 

3. list remote branches:
git branch -r


4. create a [local-branch] linked to [remote-branch]
git checkout -b local-gh-pages origin/gh-pages

[optional revert] view log:
git log
git revert sha# from log - resolve in Merge Editor - Accept Changes


5. commit changes: [do via gui] but can do terminal too:
git add .
git commit -m "Your commit message here"

6. Push commits to Remote:
git push origin gh-pages

7. Discard all changes to local branch and reclones everything
fetch origin
git reset --hard origin/gh-pages


bash:
mount c:         cd /mnt/c/
mount docs:   cd /mnt/c/Users/tonyp/Documents


Creating free blog online from github
1. [browser]            create new [blog]_repo
2. [vscode]              create new quarto [project: blog]
3. [terminal] [add]   remote repo to vscode - {git init} and do initial [commit]
4 --- perhaps we can ignore site here if its already created.
7. [vscode]              add "output-dir: docs" in [_quarto.yml: project:]
4. [vscode]              make any update+change then [render+preview]
5. [vscode]              create [.ignore] to ignore folder [/site/]
5a. [vscode]            create [_temp] and ignore it
6. [vscode]              do [second commit]
6. [vscode]              create [.ipynb] [post] folder in [/posts] then [render+preview+commit]
8. [terminal]            copy NUL .nojekyll (because you're doing everything to /docs/ [.html]
7. [terminal]            git remote add origin https://github.com/your_username/your_repo.git
7. [terminal]            push to [blog]_repo
9. [terminal]            git rm -r _site if we pushed before ignoring
5. [browser]            settings - pages - [main - root]
6. [vscode]             *** BE SURE TO SWTICH BACK TO MAIN [if you want to commit changes to main? otherwise i guess you don thave to??]*** it doesnt track your commits
7. [vscode]             any subsequent changes you should [quarto render] before publishing
7. [termianl]            this work from main and you can see changes straight away -
[quarto publish gh-pages]
8. okay i think the idea is you can [commit+push] and [deploy] a working website from [gh-pages]
9 and once you're comfortalbe it works, you can push to [main] but never actually [deploy] frm it
