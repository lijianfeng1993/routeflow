Usage of this progress:
1.install requirement:
	pip install MySQL-python
	pip install IPy

2.database open access to remote user:
	in database:
		GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '123456' WITH GRANT OPTION;
		flush privileges;

3.create database and tables:
	create database routeflow;
	use routeflow;
	create table routerinfo(name vachar(30),iplist varchar(50));
	create table routetable(network varchar(20));
	create table vminfo(name varchar(30),instance_name varchar(30),ip varchar(20),mac varchar(20));


4.python routeflow_run_add_flowtable.py 执行程序，产生数据库，在计算节点中执行流表生成和下发,最后删除数据库缓存
5.python routeflow_run_delete_flowtable.py 执行程序，产生数据库，在计算节点中执行流表删除，随后删除数据库缓存
6.python routeflow_stopslaves.py 执行程序，关闭计算节点webserver
