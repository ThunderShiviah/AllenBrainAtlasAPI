#!/bin/bash 

git log --pretty=format:'<li> <a href="https://github.com/ThunderShiviah/AllenBrainAtlasAPI/commit/master">view commit &bull;</a> date: %cd -- %s </li> ' --reverse --date=default | grep -v Merge > changelog.html

