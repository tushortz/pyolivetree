from pyolivetree import OliveTreeClient

with OliveTreeClient() as client:
    client.login()
    feed = client.store.home()
    print(feed)
