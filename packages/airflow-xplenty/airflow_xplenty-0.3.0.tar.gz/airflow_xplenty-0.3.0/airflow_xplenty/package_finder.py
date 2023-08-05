class PackageFinder:
    def __init__(self, client):
        self.client = client

    def find(self, name):
        for package in self.client.packages:
            if package.name == name:
                return package
