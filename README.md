# Offering Service

Сервис предложений позволяет пользователю получить возможные предложения по такси в зависимости от времени суток, погоды и его местоположения.

## Stack

- **FastAPI**
- **gRPC**
- **Redis**



## How to run

Пример файла **.env**

```
SERVER_PORT=8000

DB_USER=offerServiceUser
DB_NAME=offers
DB_HOST=localhost
DB_PASSWORD=offerServiceUserPassword
```



- ```make run``` локальный запуск
- ```make drun``` запуск в докер контейнере
