## Dockerfile

```Dockerfile
# line 27 ...
django-user && \
# creates a directory at /vol/web/media in the Docker container
# Media files are user uploaded files
mkdir -p /vol/web/media && \

# creates a directory at /vol/web/static in the Docker container
# Static files (CSS, JavaScript, images) for Django application
mkdir -p /vol/web/static && \

# changes the ownership of the /vol directory and all its contents (recursively with -R) to the django-user user and group.
# -R makes the command recursive
# meaning it applies the permission changes to the specified directory AND all files and subdirectories within it.
chown -R django-user:django-user /vol && \

# chmod: This is the command used to change the mode (permissions) of files and directories in Unix-like systems.
# 755: This is the permission value in octal notation, which represents:
# First digit (7): Owner permissions = read (4) + write (2) + execute (1) = 7
# Second digit (5): Group permissions = read (4) + execute (1) = 5
# Third digit (5): Others/world permissions = read (4) + execute (1) = 5
chmod -R 755 /vol
```

## app/app/settings.py

```python
# This changes the URL prefix that Django uses when referring to static files in templates.
# in a template, it will now generate URLs like /static/static/file.css
STATIC_URL = '/static/static/'
# This sets the URL prefix for user-uploaded media files.
# When need to serve uploaded files, they'll be accessible through URLs like /static/media/image.jpg
MEDIA_URL = '/static/media/'

# This defines the file system path where Django will store uploaded files.
MEDIA_ROOT = '/vol/web/media'
# This defines where Django's collectstatic command will gather all static files when deploy application
STATIC_ROOT = '/vol/web/static'
```

## docker-compose.yml

```yml
# Add to app > volumes:
# maps the Docker named volume dev-static-data to the /vol/web directory inside the container
- dev-static-data:/vol/web

# Add to volumes:
# adds the named volume dev-static-data to the top-level volumes section of the docker-compose file.
dev-static-data:

# Create a persistent storage location for your static and media files
# Ensure that these files survive container restarts or rebuilds
# Make it possible to share these files between different services (like your web app and a web server)
# Keep the data separate from the application code, following Docker best practices
```

## app/app/urls.py

```python
# Add to imports
from django.conf.urls.static import static
from django.conf import settings

# Add at the bottom
# Only runs when Django is in DEBUG mode (during development)
# Adds additional URL patterns using the += operator
# Uses the static() helper function to create patterns that serve files from MEDIA_ROOT directory
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

# 1. Enable Django to serve user-uploaded media files during development
# 2. Connect the MEDIA_URL you defined in settings.py to the actual files in MEDIA_ROOT
# 3. Make it possible to see and access uploaded files during testing and development
```

### Explanation

Process to upload & use the files:

1. Accepting uploads (saving files to disk)
2. Serving uploaded files (making them accessible via URLs)

Django will always handle the first part automatically, The issue is with the second part - serving these files.

By default, Django is designed as an application server, not a static file server. In a production environment, we'd typically configure a dedicated web server (like Nginx) to serve the static and media files efficiently.

During development, however, we don't want to set up a separate web server just for testing. This is why Django provides the static() helper function specifically for development environments.
Without these lines, here's what would happen during development:

-   Users could upload files successfully
-   The files would be saved correctly to the MEDIA_ROOT
-   But when you trying to access those files via their URLs (like viewing an uploaded image), gets a 404 error

This is why the code is conditionally added only when settings.DEBUG is True. It's a development convenience that lets us see and test uploads without setting up a separate server, but it should never be used in production (which is why it's wrapped in the DEBUG check).
