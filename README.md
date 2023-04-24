# OrderWarehouseWithCodeDuplication
This version is with code duplication in 2 separate django projects/apps    
## Setup
docker-compose up --build -d
## Task
It would be great if you can create a Django project and provide us with a link to a git repository.
Please, be aware that it's a test task, so we are not expecting a robust solution, and it's up to you how stable you want to make it.
This is a technical requirement for this project:
* Create two applications. (Store and Warehouse)
* (Store) One application should provide Orders (should be able to create order from admin page)
* (Warehouse) Another application should be able to receive these orders via the API and push back the information to the (Store).
* So when you create and order in Store, this should be synced to the Warehouse. If in warehouse you change some information this will update the information in Store (i.e. status)
* Make sure these applications can only communicate via Rest API and don't share a same database (two separate databases)
