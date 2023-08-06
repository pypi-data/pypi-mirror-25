2. Edit the ``/etc/os_cpu/os_cpu.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://os_cpu:OS_CPU_DBPASS@controller/os_cpu
