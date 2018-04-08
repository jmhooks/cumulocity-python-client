import os

# C8Y_TENANT, C8Y_USER, C8Y_PASS and C8Y_BASE_URL


def get_user():
    return os.environ.get('C8Y_USER')


def get_password():
    return os.environ.get('C8Y_PASS')


def get_tenant():
    return os.environ.get('C8Y_TENANT')


def get_base_url():
    return os.environ.get('C8Y_BASE_URL')


def get_client_id():
    return os.environ.get('C8Y_CLIENT_ID')


def get_server_host():
    return os.environ.get('C8Y_SERVER_HOST')


def get_client_model():
    return os.environ.get('C8Y_CLIENT_MODEL')


def print_env_values():
    print os.environ.get('C8Y_CLIENT_ID')
    print os.environ.get('C8Y_USER')
    print os.environ.get('C8Y_PASS')
    print os.environ.get('C8Y_TENANT')
    print os.environ.get('C8Y_BASE_URL')
    print os.environ.get('C8Y_SERVER_HOST')
    print os.environ.get('C8Y_CLIENT_MODEL')


