# initialize an astronomer project (airflow project)
astro dev init

# start the project (ensure docker engine is running)
astro dev start

# restart the project with new components, dependancies and environment etc
astro dev restart

# check which ports are in use
sudo lsof -i -P -n | grep LISTEN 

# check availability of port number eg 5432
sudo lsof -i :5432

# format the output of docker containers
# Default docker ps
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}\t{{.Ports}}\t{{.Names}}"

docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 

# check non-active containers
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -v 'Up'


# Enter airflow
astro dev bash

# test a task independently
airflow tasks test my_dag task_id 2024-01-01
airflow tasks test stock_market_v0.1 store_prices 2024-01-01


