class PackageFinder:
    PAGE_SIZE = 100

    def __init__(self, client):
        self.client = client

    def find(self, name):
        offset = 0
        while True:
            packages = self.client.get_packages(offset=offset, limit=self.PAGE_SIZE)
            if len(packages) == 0:
                return None

            for package in packages:
                if package.name == name:
                    return package

            offset += self.PAGE_SIZE
