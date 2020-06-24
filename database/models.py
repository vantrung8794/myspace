

class User():
    def __init__(self, username, avatar_url, full_name, package_id, package_name, package_cost, package_data):
        self.username = username
        self.avatar_url = avatar_url
        self.full_name = full_name
        self.package_id = package_id
        self.package_name = package_name
        self.package_cost = package_cost
        self.package_data = package_data

class FileInfo():
    def __init__(self, file_name, file_size, file_url, created_date, user_name):
        self.file_name = file_name
        self.file_size = file_size
        self.file_url = file_url
        self.created_date = created_date
        self.user_name = user_name


