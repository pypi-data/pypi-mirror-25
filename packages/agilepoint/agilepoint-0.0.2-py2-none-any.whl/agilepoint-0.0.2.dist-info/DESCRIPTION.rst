py-agilepoint
=============
Python integration for AgilePoint
---------------------------------

TODO: Create script to regenerate code

Examples
~~~~~~~~

Basic Usage::

	from agilepoint import AgilePoint
	ap = AgilePoint(host, path, username, password)
	db_info = ap.admin.get_database_info()
	# Responses in json usually have a primary key indicating what AgilePoint class the response has.
	for key, value in db_info['GetDatabaseInfoResult'].items():
	    print('{}: {}'.format(key,value))

Register Users::

	users = {'First Last': 'email@domain.tld'}
	for name, email in users.items():
	    r = ap.admin.register_user(UserName=email, FullName=name)
	    print(r)

Note: It's not well defined what arguments are required and what is optional. I've made logical conclusions. If you notice that the required/optional arguments is incorrect please submit a PR.



