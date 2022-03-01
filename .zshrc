# 毎回 "python Myserial.py" を実行するのは面倒なので、
# このファイルを.zshrcにペーストしてください
# このファイルは、zshの設定を行うファイルです。
# aliasを使ってコマンドを省略できます
# "myser csv+" のようにすると、"python Myserial.py csv+" を実行します

alias myser='cd Myserial
python Myserial.py
cd'
alias myser+='cd Myserial
python Myserial+.py
cd'