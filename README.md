# Run Gitlab webhook inside docker container

## Docker compose example

```yaml
version: "3.3"

services:
  web:
    // blah blah blah...
  webhook:
    restart: unless-stopped
    image: libert/docker-gitlab-webhook:latest
    ports:
      - 8080:80
    volumes:
      # Mount this code into /app
      - .:/app
      # Mount the docker socket
      - /var/run/docker.sock:/var/run/docker.sock:ro
      # Mount ssh key
      - /home/user/.ssh:/root/.ssh
    environment:
        REPOSITORY: drupal-composer
        TOKEN: xyzaerty
        BRANCH: test
        COMPOSE_PROJECT_NAME: my_project_directory
        POST_SCRIPT: docker-compose exec -T web /project/scripts/update.sh
```
**/!\ volumes /app and /var/run/docker.sock are required /!\**  
** .ssh directory is required if you are private project**



## Environment parameters

Parameters            | Second Header
------------          | -------------
REPOSITORY*           | Gitlab repository name
TOKEN*                | Gilab token
BRANCH*               | Git branch
COMPOSE_PROJECT_NAME  | docker-compose base dir (if use *docker-compose* in POST_SCRIPT)
PRE_SCRIPT            | Run script before git pull
POST_SCRIPT           | Run script after git pull (if launch *docker-compose exec* don't forget -T parameter)

 ** *Required parameters **

 ## Result
 ### pull result
![Pull example](https://i.imgur.com/NNJMfhD.png)
 ### POST_SCRIPT result
![Example](https://i.imgur.com/Ui8rlbr.png)
