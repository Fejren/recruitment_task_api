## Getting Started

To run the application on your local machine, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/Fejren/recruitment_task_api.git
```

2. Change into the project directory:

```bash
cd recruitment_task_api
```

3. Build and run the application using docker compose:

```bash
docker compose up --build
```

&nbsp;&nbsp; or

```bash
make up
```

4. Access the application in your browser:

```djangourlpath
http://localhost:8000/
```

<hr>

## Admin Panel

URL: http://localhost:8000/admin/ <br>

<b>Credentials: </b> <br>
Email: admin@admin.com <br>
Password: admin

<hr> 

## Endpoints

* ### Upload the image
  http://localhost:8000/api/images/

* ### Retrieve the image list
  http://localhost:8000/api/images/{user_id}

* ### Expiring link endpoint
  http://localhost:8000/api/images/link/{link_id}

<hr>
