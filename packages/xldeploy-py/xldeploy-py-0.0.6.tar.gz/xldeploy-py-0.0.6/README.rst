****************
xldeploy-py
****************
Python SDK for XL-Deploy_.

.. _XL-Deploy: https://xebialabs.com/products/xl-deploy


Usage
=======

.. code:: python

    import xldeploy

    config = xldeploy.Config(protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin")

    # If you are using url
    config = xldeploy.Config.initialize(url="http://localhost:4516/deployit", username="admin", password="admin")

    # If you are using proxies
    config = xldeploy.Config(protocol="http", host="localhost", port="4516", context_path="deployit", username="admin", password="admin",  proxy_host="localhost", proxy_port=8080, proxy_username="proxyUsername", proxy_password="proxyPassword")

    # or
    config = xldeploy.Config()
    client = xldeploy.Client(config)

    # repository
    repository = client.repository
    print repository.exists("Applications/EC2/1.0/ec2")
    print repository.exists("Applications/EC2/1.0/wrong")
    ci = repository.read("Applications/EC2/1.0/ec2")
    print ci.amiId

    # deployment
    deployment = client.deployment
    deploymentRef = deployment.prepare_initial("Applications/NIApp/1.0", "Environments/awsEnv")
    depl = deployment.prepare_auto_deployeds(deploymentRef)
    task = deployment.create_task(depl)
    task.start()
    print task.task_id

    # Deployfile

    ## Apply Deployfile script.
    deployfile = client.deployfile
    deployfile.apply(open('path_to_read_deployfile_from', 'r').read())

    ## Generate Deployfile script.

    deployfile = client.deployfile
    deployfile.generate([Environments/directory1,Environments/directory1])

Installation
============
::

    $ pip install xldeploy-py
