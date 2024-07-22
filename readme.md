# 环境

## 安装环境

〉 环境： VM + debian 11

```bash
# 安装 mysql
sudo wget https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb

sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb

sudo apt update

# 太慢
# apt-key adv --keyserver keys.gnupg.net --recv-keys 8C718D3B5072E1F5

# 干掉验证
apt -o Acquire::AllowInsecureRepositories=true update

sudo apt-get install mysql-server --fix-missing

sudo service mysql status

# 安装python3
sudo apt install python3 -y

# 安装nginx
sudo apt install nginx

```

## 配置环境

```bash
# 配置python环境
python3 -m venv venv

source venv/bin/activate

pip install Flask Flask-SQLAlchemy mysql-connector-python flask_cors
```

## 开发后端

```bash
mkdir server

touch ./server/app.py
```

## 配置脚本

〉用作同时管理前后端

```bash
mkdir scripts

touch scripts/start.bash
```

## 开发前端

> 使用的是degit + Uninen/vite-ts-tailwind-starter 模板
> 包含 ts+vite+tailwind

```bash
mkdir renderers

cd renderers/

npx degit github:Uninen/vite-ts-tailwind-starter --force

pnpm i

# 开发
pnpm run dev
```

前端代码在 renderers/src/pages/IndexPage.vue

## 配置代理

```bash
cd /etc/nginx/sites-available/

sudo touch frontend
```

通过 front.localhost.com 访问指定文件

```code
server {
    listen 80;
    listen [::]:80;

    server_name front.localhost.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr; 
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_redirect off;
    }

    location ~* \.(js|css|png|jpg|gif|swf|ico|pdf|mov|fla|zip|rar)$ {
        proxy_pass http://localhost:5173;
    }
}
```

```bash
sudo touch api
```

通过nginx 指定后端接口

```code
server {
    listen 80;
    server_name api.localhost.com;

    location / {
        proxy_pass http://localhost:5000; # 假设你的 Flask 应用运行在 5000 端口
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

软连接到 配置的文件，并修改本地开发环境的hosts 指定到开发服务器

```bash
sudo ln -s /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/

sudo systemctl restart nginx.service

sudo nano /etc/hosts
```

hosts 文件修改内容

```code
127.0.0.1 front.localhost.com
127.0.0.1 api.localhost.com
```

## 配置数据库

1、创建数据库
2、创建数据表
3、添加测试数据

```mysql&bash
# sudo mysql -u root -p

CREATE DATABASE userdatabase;

USE userdatabase;

mysql> CREATE TABLE user (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     name VARCHAR(100),
    ->     gender ENUM('male', 'female')
    -> );

mysql> insert into user (id, name, gender)
    -> values (1,'zzz','male');
Query OK, 1 row affected (0.01 sec)

```
