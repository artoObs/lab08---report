# Homework

## Часть 1

1. Создаём Dockerfile
```bash
$ touch Dockerfile
$ nano Dockerfile
```

Вставляем внутрь:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

2. `docker build -t my-web-app .`

  Вывод:
```
[+] Building 47.0s (11/11) FINISHED                              docker:default
 => [internal] load build definition from Dockerfile                       0.1s
 => => transferring dockerfile: 338B                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim         2.2s
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 2B                                            0.0s
 => [1/6] FROM docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  4.4s
 => => resolve docker.io/library/python:3.9-slim@sha256:2d97f6910b16bd338  0.1s
 => => sha256:ea56f685404adf81680322f152d2cfec62115b30dda481c 251B / 251B  0.2s
 => => sha256:fc74430849022d13b0d44b8969a953f842f59c6e9 13.88MB / 13.88MB  1.4s
 => => sha256:b3ec39b36ae8c03a3e09854de4ec4aa08381dfed84a 1.29MB / 1.29MB  0.8s
 => => sha256:38513bd7256313495cdd83b3b0915a633cfa475dc 29.78MB / 29.78MB  2.0s
 => => extracting sha256:38513bd7256313495cdd83b3b0915a633cfa475dc2a07072  1.2s
 => => extracting sha256:b3ec39b36ae8c03a3e09854de4ec4aa08381dfed84a9daa0  0.1s
 => => extracting sha256:fc74430849022d13b0d44b8969a953f842f59c6e9d1a0c2c  0.7s
 => => extracting sha256:ea56f685404adf81680322f152d2cfec62115b30dda481c2  0.0s
 => [internal] load build context                                          0.1s
 => => transferring context: 2.28kB                                        0.0s
 => [2/6] WORKDIR /app                                                     0.4s
 => [3/6] RUN apt-get update && apt-get install -y     gcc     default-l  18.8s
 => [4/6] COPY requirements.txt .                                          0.2s 
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt               6.7s 
 => [6/6] COPY . .                                                         0.1s 
 => exporting to image                                                    13.8s
 => => exporting layers                                                    8.9s
 => => exporting manifest sha256:3926fe0fd3a68d1716597a067c1d13e8460577df  0.0s
 => => exporting config sha256:14d812d67b4d865972706e0338a3f8690f8f95fce9  0.0s
 => => exporting attestation manifest sha256:74738f2acd041d4bf80206acbe95  0.1s
 => => exporting manifest list sha256:4499d3654d65f0d1f485c548e73311ae072  0.0s
 => => naming to docker.io/library/my-web-app:latest                       0.0s
 => => unpacking to docker.io/library/my-web-app:latest 
```

```bash
$ docker run -d --name my-web-container -p 5000:5000 my-web-app
```
  Вроде всё работает

3. 
```bash
$ touch README.md
$ docker cp README.md my-web-container:/home/
```
  Вывод:
```
Successfully copied 0B (transferred 1.54kB) to my-web-container:/home/
```

4. 
```bash
$ docker exec -it my-web-container /bin/bash
root@1070eae3fb5f:/app# ls /home/
```
  README здесь есть

5. 
```bash
root@1070eae3fb5f:/app# exit
```

6. `docker stop my-web-container`

  Контейнер остановлен

## Часть 2

1. Создаём docker-compose.yml в корне

```bash
version: '3.8'

services:
  web:
    build: .
    container_name: my_web_app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: myuser
      DB_PASS: mypassword
      DB_NAME: mydatabase
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: mysql:8.0
    container_name: my_mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-prootpassword"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
```

2. `$ docker compose up --build`

3. По адресу http://localhost:5000 видно содержимое. Есть проблема с русским языком, но это связано с самой системой. По какой-то причине мне просто не даёт поставить русский язык и не получается нормально ввести в mysql.
   <img width="515" height="161" alt="Снимок экрана 2026-05-29 031710" src="https://github.com/user-attachments/assets/c852692a-f1a0-41e3-a1df-c2b1754d00eb" />


4. `$ docker compose down`
  Контейнер остановлен
