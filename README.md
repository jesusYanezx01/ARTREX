
## Project Startup Guide

Before you begin, make sure you have a basic understanding of Docker Compose.

### Step 1: Launch the Containers

Run the following command to build and launch the containers in the background:

```bash
docker compose up -d --build
```

### Step 2: Verify that the Containers are Running

After running the above command, make sure the containers are running correctly.

You can verify this with:

```bash
docker compose ps
```

### Step 3: Run the Database Migration

Enter the backend container to run the migrations:

```bash
docker exec -it <backend_container_name> bash
```

Once inside the container, start the Flask shell:

```bash
flask db upgrade
```

### Step 4: Populating the Database

After running the migrations, populate the database using the following command:

```bash
flask shell
```

Inside the shell, run:

```python
exec(open('scripts/populate_data.py').read())
```
