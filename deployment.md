# Deployment docs:
> The application deployment on **VPS**

In this application will I deploy AWS EC2 instance.

- Login AWS console.
- Create and lunch new instance.

Once you are inside the remote machine we need to install Python and NGINX.

###### Issue the following commands on the terminal:
```bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
sudo -H pip3 install --upgrade pip
```
Next up we need to bind our application to a gunicorn module that serves as an interface to your application, translating client requests from HTTP to Python calls that your application can process.
So we start by creating a socket file:
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
```bash
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Save and close that file. Next we create a service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following code to it:
```bash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/apiv1
ExecStart=/home/ubuntu/apiv1/env/bin/gunicorn \
          --access-logfile - \
          --workers 5 \
          --bind unix:/run/gunicorn.sock \
          --worker-class uvicorn.workers.UvicornWorker \
          app:app

[Install]
WantedBy=multi-user.target
```
Save and close as well.
Next start the Gunicorn socket:

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
Now that Gunicorn is set up, next we’ll configure Nginx to pass traffic to the process.
Start by creating and opening a new server block in Nginx’s sites-available directory:

```bash
sudo nano /etc/nginx/sites-enabled/api
```
Add the following lines to it:
```bash
server {
    listen 80;
    server_name server_domain_or_IP;
    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Save this file as well. Test that the config is okay by:

```bash
sudo nginx -t
```

If all is well then we need to restart the services so go aheda and:

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```
