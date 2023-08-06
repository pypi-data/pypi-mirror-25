"""
Decorator for setup task
"""


from fabric.api import task, settings, hide
from py_mina.config import check_deploy_config
from py_mina.tasks.setup import *
from py_mina.echo import echo_task


def setup_task(fn):
	"""
	Setup task function decorator
	"""

	def setup(*args):
		"""
		Runs setup process on remote server
		"""

		echo_task('Running "setup" task')

		check_deploy_config()

		with settings(hide('output'), colorize_errors=True):
			create_required()
			create_shared()
			add_repo_to_known_hosts()
			add_host_to_known_hosts()

			fn(*args)

	# Copy __name__ and __doc__ from decorated function to decorator function
	setup.__name__ = fn.__name__
	if fn.__doc__: setup.__doc__ = fn.__doc__

	# Decorate with "fabric" @task decorator
	return task(setup)
