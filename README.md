# fastAPICRUD
> Fast API CRUD backend web application.

### Setup:
If you want to run the project in your local development server please follow the instruction.

###### Open your terminal:

- python 3.10
- sqlalchemy

```bash
git clone https://github.com/mbrsagor/fastAPICRUD.git
cd fastAPICRUD
virtualenv venv --python=python3.10
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host localhost --port 8000 --reload
```

#### Run docker::
```bash
docker-compose up -d
```

###### An ORM for Python::
```bash
pip install SQLAlchemy fastapi-utils
```


```python
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Source:
[Here is the blog which I founded](https://codevoweb.com/build-a-crud-app-with-fastapi-and-sqlalchemy/)
