from pymental.client import Conductor

client = Conductor()
job = client.jobs.get(210, clean=True)

for _ in range(5):
    client.jobs.create(instance=job)
    print('created ')
