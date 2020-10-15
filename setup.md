
# Setup Smart4L application

IP : 13.59.162.131
PORT : 443
REDIRECTION : 80 -> 443
DOMAIN : 
	api.aws.cbarange.ovh
FLASK IP: 127.0.0.1
	ws.aws.cbarange.ovh
FLASK PORT: 8520
WEBSOCKET IP: 127.0.0.1
WEBSOCKET PORT: 8530

## Directory structure
```bash
sudo mkdir /logs
sudo mkdir /app
sudo chown ubuntu /logs
sudo chown ubuntu  /app 
mkdir /app/smart4l/
mkdir /app/smart4l/front
mkdir /app/smart4l/back
mkdir /app/smart4l/ssl
mkdir /logs/smart4l/
mkdir /logs/smart4l/apache2
```
## Install dependencies
```bash
sudo apt install certbot
sudo apt install python3
sudo apt install git
```

## SSL Configuration
```bash
# Test your commande with dry-run option, use staging environment, production rate Failed Validation is 5
sudo certbot certonly --manual --cert-name ws_cert -d *.aws.cbarange.ovh \
--register-unsafely-without-email  --preferred-challenges dns --dry-run

sudo certbot certonly --manual --cert-name ws_cert -d *.aws.cbarange.ovh \
--register-unsafely-without-email --preferred-challenges dns

```
## Apache Configuration
```bash

# ---------------------------------------------------------
# ---                    DEFAULT GATEWAY                ---
<VirtualHost *:443 *:80>
        DocumentRoot /var/www/html/default_gateway
        ErrorLog /logs/smart4l/apache2/default_gateway_error.log
        CustomLog /logs/smart4l/apache2/default_gateway_access.log combined
</VirtualHost>

# ---------------------------------------------------------
# ---                   WEBSOCKET GATEWAY               ---
<VirtualHost *:443>
	ServerName ws.aws.cbarange.ovh
    ErrorLog /logs/smart4l/apache2/websocket_error.log
    CustomLog /logs/smart4l/apache2/websocket_access.log combined
    ProxyPass / https://127.0.0.1:8530/
	ProxyPassReverse / https://127.0.0.1:8530/
	SSLEngine on
    SSLCertificateFile /app/smart4l/ssl/your_domain_name.crt
    SSLCertificateKeyFile /app/smart4l/ssl/your_private.key
</VirtualHost>

# ---------------------------------------------------------
# ---                     FLASK GATEWAY                 ---
<VirtualHost *:443>
	ServerName ws.aws.cbarange.ovh
    ErrorLog /logs/smart4l/apache2/websocket_error.log
    CustomLog /logs/smart4l/apache2/websocket_access.log combined
    ProxyPass / https://127.0.0.1:8520/
	ProxyPassReverse / https://127.0.0.1:8520/
	SSLEngine on
    SSLCertificateFile /app/smart4l/ssl/your_domain_name.crt
    SSLCertificateKeyFile /app/smart4l/ssl/your_private.key
</VirtualHost>

```

## Git Configuration
```bash

```
## Python Configuration
```bash

```

```bash

```

