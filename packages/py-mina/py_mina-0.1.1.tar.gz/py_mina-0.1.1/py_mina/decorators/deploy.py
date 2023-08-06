"""
Decorator for deploy task
"""


from __future__ import with_statement
from fabric.api import task, settings
from py_mina.config import check_deploy_config
from py_mina.state import state, set_state
from py_mina.exceptions import *
from py_mina.tasks.deploy import *
from py_mina.echo import echo_task

def deploy_task(on_launch=None):
	"""
	Deploy task arguments decorator
	"""

	def deploy_task_fn(fn):
		"""
		Deploy task function decorator
		"""

		def pre_deploy():
			with settings(abort_exception=PreDeployError):
				try: 
					check_lock()
					lock()
					create_build_path()
					discover_latest_release()

					set_state('pre', True)
				except PreDeployError: 
					set_state('pre', False)


		def post_deploy():
			with settings(abort_exception=PostDeployError):
				try:
					if state.get('deploy') == True:
						move_build_to_releases()
						link_release_to_current()

					set_state('post', True)
				except PostDeployError: 
					set_state('post', False)


		def finallize_deploy():
			with settings(abort_exception=FinallizeDeployError):
				try: 
					if state.get('deploy') == True:
						cleanup_releases()
					remove_build_path()
					unlock()

					set_state('finallize', True)
				except Exception:
					set_state('finallize', False)


		def launch():
			if not on_launch == None and callable(on_launch):
				with settings(abort_exception=LaunchError):
					try: 
						on_launch()

						set_state('launch', True)
					except LaunchError:
						set_state('launch', False)


		def deploy(*args):
			"""
			Runs deploy process on remote server
				1) Pre deploy (lock, build path, latest_release)
				2) Deploy
				3) Post deploy (move to releases, link release to current)
				4) Finallize deploy (cleanup, remove build path, unlock)
				5) Launch application
				6) Show deploy stats
			"""
			
			check_deploy_config()

			with settings(colorize_errors=True):
				try:
					pre_deploy()

					with cd(fetch('build_to')), settings(abort_exception=DeployError):
						try:
							fn(*args)
							set_state('deploy', True)
						except DeployError: 
							set_state('deploy', False)

					post_deploy()
				finally:
					finallize_deploy()

			# Launch application if build succeeded
			if state.get('deploy') == True and state.get('post') == True: 
				launch()

			# Show deploy stats
			print_deploy_stats()

		# Copy __name__ and __doc__ from decorated function to decorator function
		deploy.__name__ = fn.__name__
		if fn.__doc__: deploy.__doc__ = fn.__doc__

		# Decorate with "fabric" @task decorator
		return task(deploy)

	return deploy_task_fn
