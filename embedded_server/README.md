# Partie Embarquée

Cette branche héberge la partie embarquée, connexion aux capteurs, services automatiques, serveur.

## 5 niveaux

### Interface → ReactJS

Branch : web-client

### API → Python, afin de récupérer les mesures en temps réel

Folder : smart4l_api

### Service enregistrement en base + broadcast RabbitMQ + automatisation (loop infinie)

Folder : smart4l_service

### API mesure + activation (pas utile en vrai)

Folder : metering_api

### Modules de connexion aux capteurs

Folder : sensor_camera-module