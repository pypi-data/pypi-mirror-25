# django-requestuser

Usage:

add requestuser.RequestUserMiddleware to your middleware

    MIDDLEWARE_CLASSES = [
        ...
        'requestuser.RequestUserMiddleware'
    ]


now you can get current user via:

    from requestuser import get_request_user

    user = get_request_user()

