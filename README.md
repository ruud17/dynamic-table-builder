## Dynamic-Table-Builder

This solution offers a RESTful service for generating dynamic models on the fly within a database schema in real-time. 
It was developed using the Python programming language along with the Django framework. 
The approach involves utilizing the [type()](https://www.geeksforgeeks.org/create-classes-dynamically-in-python/) function as well as [SchemaEditor](https://docs.djangoproject.com/en/4.0/ref/schema-editor/) to dynamically configure models and schema changes, similar to the conventional approach of using Django migrations. 
As a result, users are able to define only the `table_name` and `fields`, leading to the automatic creation of both the dynamic model and the corresponding database table, eliminating the need for predefined static model classes.

## API endpoints

| Request Type | Endpoint | Body Payload                                                                                             |
| :---         |     :---     |:---------------------------------------------------------------------------------------------------------|
| POST (create dynamic table)  | /api/table     | ```{"table_name": "person",   "fields": { "name": "string", "age": "number"}}```                         |
| PUT (update dynamically created table)    | /api/table/:id       | ```{"fields": { "name": "string", "age": "number"}}```  <br/> where :id is the name of table, e.g person |
| POST  (insert records in dynamically created tables)   | /api/table/:id/row      | ```{"name": "Person1","age" :54} ```                                                                     |
| GET (get records from dynamically created tables)    | /api/table/:id/rows    |                                                                                                          |


## Prerequisites
- [Python](https://www.python.org/downloads/) version 3.x
- [Django](https://www.djangoproject.com/) version 4.x.x
- [PostreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) - select a version for your OS
- optional [pgAdmin](https://www.pgadmin.org/download/) 


## Instalation

- Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) package
- `````
  $ virtualenv <env_name>
  $ source <env_name>/bin/activate
  (<env_name>)$ pip install -r path/to/requirements.txt

- Ensure PostgreSQL is running under configured settings in `backed/settings.py` - DATABASES property

## Additional
(For testing purposes) - Within the main directory, you'll discover the Postman collection that can be effortlessly imported into your Postman tool. This collection enables you to effectively assess the API endpoints.
