Prerequisites
-------------

Before you install and configure the replace with the service it implements service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``os_cpu`` database:

     .. code-block:: none

        CREATE DATABASE os_cpu;

   * Grant proper access to the ``os_cpu`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON os_cpu.* TO 'os_cpu'@'localhost' \
          IDENTIFIED BY 'OS_CPU_DBPASS';
        GRANT ALL PRIVILEGES ON os_cpu.* TO 'os_cpu'@'%' \
          IDENTIFIED BY 'OS_CPU_DBPASS';

     Replace ``OS_CPU_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``os_cpu`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt os_cpu

   * Add the ``admin`` role to the ``os_cpu`` user:

     .. code-block:: console

        $ openstack role add --project service --user os_cpu admin

   * Create the os_cpu service entities:

     .. code-block:: console

        $ openstack service create --name os_cpu --description "replace with the service it implements" replace with the service it implements

#. Create the replace with the service it implements service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        replace with the service it implements public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements admin http://controller:XXXX/vY/%\(tenant_id\)s
