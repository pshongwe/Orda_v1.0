# Set the number of worker processes
workers = 4

# Bind the server to this host and port
bind = '127.0.0.1:5000'

# Set the path to your Flask application
app = 'app:app'

# Logging configuration (optional)
errorlog = '/path/to/error.log'
accesslog = '/path/to/access.log'
