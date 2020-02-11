def join_url_paths(self, *paths):
    return '/'.join(path.strip('/') for path in paths if path)
