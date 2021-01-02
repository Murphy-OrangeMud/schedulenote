# schedulenote
软件工程实践项目.

## 用法：

`git clone https://github.com/Murphy-OrangeMud/schedulenote.git`

`pip3 install -r requirements.txt`

`uwsgi --ini uwsgi.ini`


## 前端部署：
`ssh se_gp13@8.136.141.151 `

输入密码：se_gp13

`cd ~/temp/front-end/schedulenote`

`sudo git fetch origin master`

`sudo git pull origin master`

（如果pull失败，先使用git reset --hard 再pull）

`sudo npm run build`

`sudo cp -r ~/temp/front-end/schedulenote/dist /usr/local/nginx -rf`

就能更新前端html了