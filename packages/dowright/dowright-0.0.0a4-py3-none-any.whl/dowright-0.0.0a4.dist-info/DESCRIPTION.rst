.. image:: https://bytebucket.org/dogwynn/dowright/raw/master/dowright.png
   :align: right


DOwright
========

Simple YAML-based specification for creation and configuration of
DigitalOcean droplets

What is this for?
-----------------

This tool/library exists to:

* provide a straightforward way to specify a particular set of
  DigitalOcean droplets and, given that specification,

* create/destroy them in an idempotent manner and

* provide an Ansible inventory for those droplets.

The work was motivated by the "chicken/egg" problem of using a
configuration management tool like Ansible on a yet-uncreated
DigitalOcean droplet/service cluster. Ansible is certainly useful for
deploying a configuration to an existing set of resources, and it even
has an API for creating those resources on DigitalOcean.

However, there wasn't a straightforward way of using Ansible to both
create and configure the resources without having an inventory file
hand-written prior to creation. If you changed the number of created
droplets, you would have to hand-edit the inventory. With this
tool, an existing set of Ansible roles can be used on a dynamic set of
DigitalOcean droplets.

``dowright`` is for Python 3.4+ only with no plans for backwards
compatibility.


Installation
------------

* Install using ``pip3``::

    pip3 install dowright

* Initialize the ``.tokenmanager.yml`` file in your home directory::

    python3 -m tokenmanager -i

* Provide a ``digitalocean`` token namespace in your
  ``.tokenmanager.yml`` file. Then provide as many sub-namespaces as
  you need for your YAML specifications. These will then be specified
  in your YAML using the ``token`` key. E.g. ::

    digitalocean:
      app1: a1e1c084540b51b33af3c6b63d48ede2937c8df92f7e6e3beb1f630ac750b851
      app2: 03593464105708646cc04d847ffc81c5b7775c462f68b573f2aff5d933635e17

Usage
-----

To use ``dowright``, you will need to create a YAML specification for
your DigitalOcean resources. Here's an example spec (named
``my_web_app.yml``)::

  # token: this specifies which token reference under the
  #   "digitalocean" token group should be used for creating
  #   the droplets specified 
  token: app1 # using the above example of a .tokenmanager.yml file

  # prefix: is used to namespace your resources and is also
  #   provided as a tag for these resources at creation time
  prefix: my_web_app 

  # droplets: is a dictionary of named groups of resources. Each group
  #   corresponds to an Ansible inventory group and can be referenced
  #   as a group in various ways in this specification. 
  droplets:
    # Groups are lists of dictionaries that correspond to the creation
    #   parameters of the droplets to be created. Group names are also
    #   added as tags at creation time.
    data:
      - name: data[01:10]  # can use Ansible-style name expansions
                           # to create multiple droplets with the same
                           # name prefix and parameters
        size_slug: 2gb  # each key in the dictionary corresponds 1-to-1
                        # with the parameters given in the DigitalOcean
                        # droplet creation REST API 
        volumes:
          - aaaaaaaa-bbbb-ffff-3333-000000000000

        # cloud_config_commands: is a special key that will be
        #   transformed into the "#cloud-config" YAML-formatted string
        #   under the "user_data" parameter. It is a list of bash shell
        #   commands that will be placed in the "runcmd" list of the
        #   "#cloud-config" string. In order to track completion of
        #   these commands, a final command (that creates a sentinel
        #   file "/.cloud-config-done") is appended by dowright.
        cloud_config_commands:
          - mkdir /data
          - mount -o defaults,nofail /dev/disk/by-id/scsi-0DO_Volume_volume-nyc1-01-part1 /data
          - >-
            echo "/dev/disk/by-id/scsi-0DO_Volume_volume-nyc1-01-part1 /data xfs defaults,nofail 0 2" >> /etc/fstab
          - apt update
          - apt install -y python3 python3-pip
          - pip3 install --upgrade pip
    nameserver:
      - name: ns
        image: ubuntu-16-04-x64

  # defaults: these are default creation parameters for all resources
  defaults:
      image: ubuntu-17-04-x64
      size_slug: 1gb
      region: nyc1
      ssh_keys:
        - 999999
        - 999998
      private_networking: yes

  # floating_ips: these are mappings of previously-created floating IPs 
  #   to be mapped to particular droplets. *Notice*: the name given here
  #   corresponds to that given under the above "droplets:" section.
  #   It does /not/ have the "prefix:" string (e.g. "my_web_app"
  #   given above). 
  floating_ips:
    192.16.1.1: data01
    192.16.1.2: ns

  # domains: mappings of DigitalOcean-managed domains to a list of 
  #   creation parameters for subdomains
  domains:
    mydomin.com:
      - type: 'A'
        name: 'ds_master'
        data: data01
      - type: 'A'
        name: 'ns_master'
        data: ns

  # inventory: this defines the Ansible inventory for the
  #   DigitalOcean droplets.   
  inventory:
    # name: filename of inventory
    name: hosts.conf
    # groups: group definitions in inventory
    groups:
      # each group is a list of references to DigitalOcean droplets
      "datanodes:children":
        - name: data   # references can be to droplet groups
      namenodes:
        - name: nameserver 
      hadoop_startup:
        - name: ns     # references can be to individual droplet names
      "nodemanagers:children":
        - name: datanodes  # if the inventory group name has a colon
                           #   in it (i.e. it's a group of inventory
                           #   groups), then the reference must be to
                           #   another inventory group
      "hadoop:children":
        - name: namenodes
        - name: datanodes
      analysis:
        - name: data01


To create/build the droplets specified::

  python3 -m dowright my_web_app.yml -b

To wait for completion of droplet creation::

  python3 -m dowright my_web_app.yml -w

To link floating IPs to DigitalOcean droplets::

  python3 -m dowright my_web_app.yml -i

To link DigitalOcean-managed domains to droplets::

  python3 -m dowright my_web_app.yml -d

To create the Ansible inventory for your droplets::

  python3 -m dowright my_web_app.yml -c

To do all the above::

  python3 -m dowright my_web_app.yml -bwidc

To destroy the DigitalOcean droplets specified in your YAML::

  python3 -m dowright my_web_app.yml --destroy


