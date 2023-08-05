class DeployfileService:
    __path = "/deployfile"

    def __init__(self, http_client):
        self.http_client = http_client
        self.headers = {'content-type': 'text/plain', 'Accept': 'text/plain'}

    def get_path(self, *args):
        return "/".join([self.__path] + list(args))

    def generate(self, directories):
        params = {"folder": directories}
        return self.http_client.get(path=self.get_path("generate"),
                                    headers=self.headers,
                                    params=params)

    def apply(self, deployfile):
        post = self.http_client.post(path=self.get_path("apply"), headers=self.headers, body=''.join(map(str, deployfile)))
        return post
