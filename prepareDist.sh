rm -rf dist
mkdir dist
mkdir dist/aws
mkdir dist/aws_server
mkdir dist/aws_login_server

#Make client dist
cp Client/*.py dist/aws
cp -R Client/res dist/aws
cp Client/TankStats.db dist/aws

#Make Server dist
cp Server/*.py dist/aws_server
cp Server/TankStats.db dist/aws_server
rm dist/aws_server/loginServer.py
rm dist/aws_server/launchLoginServer.py

#Make login server dist
cp Server/launchLoginServer.py dist/aws_login_server/aws_login_server.py
cp Server/LoginDatabase dist/aws_login_server
cp Server/loginServer.py dist/aws_login_server

#Copy login config
cp updateAllSettingsDist.py dist
python2 dist/updateAllSettingsDist.py
