.. link: 
.. description: 
.. tags: 
.. date: 2013/04/17 16:26:48
.. title: Simply generating self-signed SSL Certs with Ansible
.. slug: simply-generating-self-signed-ssl-certs-with-ansible

I've really been enjoying using `Ansible <http://ansible.cc>`_ for my personal sysadmin tasks. Puppet is still great, and it's what I still use in our large infrastructures, but for one-offs and personal services Ansible seems to really fit what I need.

But today's quick tip is something that took me a bit of time to track down -- making a simple self-signed SSL certficate for a node.

And, it's this easy. In the ``tasks`` of a playbook:

.. code:: yaml

    - name: create self-signed SSL cert
      command: openssl req -new -nodes -x509 -subj "/C=US/ST=Oregon/L=Portland/O=IT/CN=${ansible_fqdn}" -days 3650 -keyout /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.crt -extensions v3_ca creates=/etc/nginx/ssl/server.crt
      notify: reload nginx

The cert will only be generated if ``/etc/nginx/ssl/server.crt`` is missing, so if you typo something, you'll have to remove it on the server side. It uses the ``ansible_fqdn`` fact; you could replace this with whatever you'd like if, for example, you're load balancing this host.
