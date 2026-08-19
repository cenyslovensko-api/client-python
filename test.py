import cenyslovensko_client

if __name__ == '__main__':
    with cenyslovensko_client.clients.CenyslovenskoVersionRpcClient() as client:
        println(client.get_version())
