from flask import current_app


def auth(key, ip):
    if key == current_app.config.get('AUTH_KEY'):
        return True
    else:
        return False
