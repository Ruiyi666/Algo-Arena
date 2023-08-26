# -*- mode: ruby -*-
# vi: set ft=ruby :

# A Vagrantfile to set up two VMs, a frontend and a database server,
# connected together using an internal network with manually-assigned
# IP addresses for the VMs.

# Typical `vagrant up` seems to assume the Docker provider anyway, but
# `vagrant up --provider=docker` would be even more explicit.
# Thanks to https://github.com/rofrano/vagrant-docker-provider

Vagrant.configure("2") do |config|
    # (We have used this box previously, so reusing it here should save a
    # bit of time by using a cached copy.)
    config.vm.box = "ubuntu/focal64"
  
    config.vm.provider :docker do |docker, override|
      override.vm.box = nil
      docker.image = "dme26/vagrant-provider:ubuntu-focal"
      docker.remains_running = true
      docker.has_ssh = true
      docker.privileged = true
      docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
      docker.create_args = ["--cgroupns=host"]
      # The create_args can be augmented to set the container's hostname
      # Note that the actual following example has not been tested.
      #docker.create_args = ["--cgroupns=host","-h somehostname.localdomain"]
      # Uncomment to force arm64 for testing images on Intel
      # docker.create_args = ["--platform=linux/arm64"]     
    end
    
    # this is a form of configuration not seen earlier in our use of
    # Vagrant: it defines a particular named VM, which is necessary when
    # your Vagrantfile will start up multiple interconnected VMs. I have
    # called this first VM "frontend" since I intend it to run the
    # frontend (unsurprisingly...).
    config.vm.define "frontend" do |frontend|
      # These are options specific to the frontend VM
      frontend.vm.hostname = "frontend"
      
      # This type of port forwarding has been discussed elsewhere in
      # labs, but recall that it means that our host computer can
      # connect to IP address 127.0.0.1 port 8080, and that network
      # request will reach our frontend VM's port 80.
      frontend.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
      
      # We set up a private network that our VMs will use to communicate
      # with each other. Note that I have manually specified an IP
      # address for our frontend VM to have on this internal network,
      # too. There are restrictions on what IP addresses will work, but
      # a form such as 192.168.2.x for x being 11, 12 and 13 (three VMs)
      # is likely to work.
      frontend.vm.network "private_network", ip: "192.168.56.11"
  
      # This following line is only necessary in the CS Labs... but that
      # may well be where markers mark your assignment.
      frontend.vm.synced_folder ".", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]
  
      # Now we have a section specifying the shell commands to provision
      # the frontend VM. Note that the file test-website.conf is copied
      # from this host to the VM through the shared folder mounted in
      # the VM at /vagrant
      frontend.vm.provision "shell", path: "build-frontend-vm.sh"
    end
    
    # Here is the section for defining the backend server, which I have
    # named "backend".
    config.vm.define "backend" do |backend|
      backend.vm.hostname = "backend"
      # Note that the IP address is different from that of the frontend
      # above: it is important that no two VMs attempt to use the same
      # IP address on the private_network.
      backend.vm.network "private_network", ip: "192.168.56.12"
      backend.vm.synced_folder ".", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]

      backend.vm.provision "shell", path: "build-backend-vm.sh"
    end

    # Here is the section for defining the database server, which I have
    # named "dbserver".
    config.vm.define "dbserver" do |dbserver|
      dbserver.vm.hostname = "dbserver"
      # Note that the IP address is different from that of the frontend
      # above: it is important that no two VMs attempt to use the same
      # IP address on the private_network.
      dbserver.vm.network "private_network", ip: "192.168.56.13"
      dbserver.vm.synced_folder ".", "/vagrant", owner: "vagrant", group: "vagrant", mount_options: ["dmode=775,fmode=777"]
      
      dbserver.vm.provision "shell", path: "build-dbserver-vm.sh"
    end
  
  end
  
  #  LocalWords:  frontend xenial64
  