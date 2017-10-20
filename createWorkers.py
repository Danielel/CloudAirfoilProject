# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
from cinderclient import client as ciclient
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavorT = "ssc.small" 
private_net = "SNIC 2017/13-45 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
da_key = 'denialKey2'
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"

#auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'], username=env['OS_USERNAME'], password=env['OS_PASSWORD'],  project_name=env['OS_PROJECT_NAME'], project_domain_name=env['OS_USER_DOMAIN_NAME'], project_id=env['OS_PROJECT_ID'], user_domain_name=env['OS_USER_DOMAIN_NAME'])
def createWorker(instanceName):
    loader = loading.get_plugin_loader('password')

    auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                    username=env['OS_USERNAME'],
                                    password=env['OS_PASSWORD'],
                                    project_name=env['OS_PROJECT_NAME'],
                                    project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                    project_id=env['OS_PROJECT_ID'],
                                    user_domain_name=env['OS_USER_DOMAIN_NAME'])

    sess = session.Session(auth=auth)
    nova = client.Client('2.1', session=sess)
    cinder = ciclient.Client('2', session=sess)#user, pswd, project_name, keystone_link, region_name = region_name)
    
    
    print ("user authorization completed.")
    
    #description =instanceName + "-vol",
    volume = cinder.volumes.create(15, description = instanceName + "-vol", source_volid='a8944f8e-ba3b-417a-9645-4c4929241e26')
    block_device_mapping = {'vda':volume.id}
    
    image = nova.glance.find_image(image_name)
    
    #volume = nova.cinder.find_block block_device_mapping
    key = nova.keypairs.get(da_key)
    
    flavor = nova.flavors.find(name=flavorT)
    #key_pair = client_manager.compute.keypairs
    

    if private_net != None:
        net = nova.neutron.find_network(private_net)
        nics = [{'net-id': net.id}]
    else:
        sys.exit("private-net not defined.")

    #print("Path at terminal when executing this file")
    #print(os.getcwd() + "\n")
    cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
    if os.path.isfile(cfg_file_path):
        userdata = open(cfg_file_path)
    else:
        sys.exit("cloud-cfg.txt is not in current working directory")

    secgroups = ['default', 'ACC9-serverSG']

    while(str(volume.status) == 'creating'):
        volume = cinder.volumes.get(volume.id)
        time.sleep(0.5)
    print ("Creating instance ... ")
    instance = nova.servers.create(name=instanceName, image=image, flavor=flavor, userdata=userdata, nics=nics, key_name=key.name, block_device_mapping = block_device_mapping, security_groups=secgroups)
    inst_status = instance.status
    print ("waiting for 10 seconds.. ")
    time.sleep(10)

    while inst_status == 'BUILD':
        print( "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
        time.sleep(3)
        instance = nova.servers.get(instance.id)
        inst_status = instance.status

    print ("Instance: "+ instance.name +" is in " + inst_status + "state")
    userdata.close()
    return (instance.id, volume.id)

def killWorker(instanceId, volumeId):
    loader = loading.get_plugin_loader('password')

    auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                    username=env['OS_USERNAME'],
                                    password=env['OS_PASSWORD'],
                                    project_name=env['OS_PROJECT_NAME'],
                                    project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                    project_id=env['OS_PROJECT_ID'],
                                    user_domain_name=env['OS_USER_DOMAIN_NAME'])

    sess = session.Session(auth=auth)
    nova = client.Client('2.1', session=sess)
    cinder = ciclient.Client('2', session=sess)#user, pswd, project_name, keystone_link, region_name = region_name)
    print("deleting instance....")
    nova.servers.delete(instanceId)
    volume = cinder.volumes.get(volumeId)
    print(volume.status)
    while(str(volume.status) == 'migrating' or str(volume.status) == 'attached' or str(volume.status) == 'in-use'):
        volume = cinder.volumes.get(volume.id)
        time.sleep(0.5)
    print("deleting volume....")
    cinder.volumes.delete(volumeId)
    
if __name__ == '__main__':
    
    x = createWorker("blalba")
    time.sleep(10)
    killWorker(x[0], x[1])
