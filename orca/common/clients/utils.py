def join_url_paths(*paths):
    return "/".join(path.strip("/") for path in paths if path)
