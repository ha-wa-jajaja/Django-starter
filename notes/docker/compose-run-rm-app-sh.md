## `docker compose run --rm app sh`

### Params

<ol>
    <li><strong>docker compose run</strong> - This is the base command that runs a one-off command on a service defined in your <code>docker-compose.yml</code> file.</li>
    <li><strong>--rm</strong> - This flag tells Docker to automatically remove the container when it exits. Without this flag, stopped containers would remain in the system and take up resources.</li>
    <li><strong>app</strong> - This refers to the specific service name defined in your <code>docker-compose.yml</code> file that you want to run the command against.</li>
    <li><strong>sh</strong> - This is the actual command you're requesting to run inside the container, which in this case launches a shell session.</li>
</ol>

### Execution

-   Create a container from the image defined for the "app" service in docker-compose.yml
-   Run the specified command (sh in this case) in that container
-   The container will remain active only as long as that command is running
