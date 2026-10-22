# Troubleshooting notes

A database connection refused error suggests the database endpoint is unreachable or not accepting connections; verify service health, host, and port before claiming a root cause.
A duplicate key error on users_email_key means the operation conflicts with an existing unique email value; inspect validation and error handling and consider returning an appropriate client error.
A cache unavailable warning can be recoverable when the application falls back to the database; correlate request IDs and final status before linking it to a failure.
A status 500 alone does not establish a cause; request the stack trace, application error details, and correlated database logs.
