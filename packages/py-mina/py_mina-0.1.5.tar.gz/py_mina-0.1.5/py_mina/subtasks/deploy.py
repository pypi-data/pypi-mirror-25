"""
Deploy tasks
"""

from __future__ import with_statement
import os
from fabric.colors import red, green, yellow
from fabric.api import *
from py_mina.config import fetch, ensure, set, check_config
from py_mina.state import state
from py_mina.echo import *


################################################################################
# Config
################################################################################


def check_deploy_config():
	"""
	Check required config settings for deploy task
	"""

	check_config(['user', 'hosts', 'deploy_to', 'repository', 'branch'])


################################################################################
# Pre deploy hooks
################################################################################


def check_lock():
	"""
	Aborts deploy if lock file is found
	"""
	
	echo_subtask("Checking `deploy.lock` file presence")

	with cd(fetch('deploy_to')), settings(hide('everything'), warn_only=True):
		if run('test -f deploy.lock').succeeded:
			abort("Another deploy in progress")


def lock():
	"""
	Locks deploy
	Parallel deploys are not allowed
	"""

	ensure('build_to')

	echo_subtask("Creating `deploy.lock` file")

	with cd(fetch('deploy_to')):
		run('touch deploy.lock')


def create_build_path():
	"""
	Creates tmp dir for building app. 

	Folder will be:
		* deleted -> if build fails
		* moved to releases -> if build succeeds
	"""
	
	ensure('build_to')

	echo_subtask("Creating build path")

	with settings(hide('warnings'), warn_only=True):
		build_path = fetch('build_to')

		if run('test -d %s' % build_path).failed:
			run('mkdir -p %s' % build_path)


def discover_latest_release():
	"""
	Connects to remote server and discovers next release number
	"""

	ensure('releases_path')

	releases_path = fetch('releases_path')

	echo_subtask("Discovering latest release number")

	# Get latest release number
	with settings(hide('warnings'), warn_only=True):
		if run('test -d %s' % releases_path).failed:
			last_release_number = 0
			
			run('mkdir -p %s' % releases_path)
		else:
			releases_respond = run('ls -1p %s | sed "s/\///g"' % releases_path)
			releases_dirs = list(filter(lambda x: len(x) != 0, releases_respond.split('\r\n')))

			if len(releases_dirs) > 0:
				last_release_number = max(map(lambda x: int(x), releases_dirs)) or 0
			else:
				last_release_number = 0

	release_number = last_release_number + 1

	# Set release info to config 
	set('release_number', release_number)
	set('release_to', os.path.join(releases_path, str(release_number)))


################################################################################
# Deploy
################################################################################


def link_shared_paths():
	"""
	Links paths set in shared_dirs and shared_files.
	"""

	ensure('build_to')
	ensure('shared_path')
	ensure('shared_dirs')
	ensure('shared_files')

	echo_subtask("Linking shared paths")

	with cd(fetch('build_to')):
		shared = fetch('shared_path')

		# Shared dirs
		for sdir in fetch('shared_dirs'):
			relative_path = os.path.join('./', sdir)
			directory, filename_ = os.path.split(relative_path)
			shared_path = os.path.join(shared, sdir)
		
			run('mkdir -p %s' % directory)
			run('rm -rf %s' % relative_path)
			run('ln -s "{0}" "{1}"'.format(shared_path, relative_path))

		# Shared files
		for sfile in fetch('shared_files'):
			shared_path = os.path.join(shared, sfile)
			relative_path = os.path.join('./', sfile)
			directory, filename_ = os.path.split(relative_path)

			run('mkdir -p %s' % directory)
			run('ln -sf "{0}" "{1}"'.format(shared_path, relative_path))


################################################################################
# Post deploy hooks
################################################################################


def move_build_to_releases():
	"""
	Moves current build folder to releases path
	"""

	ensure('build_to')
	ensure('release_to')

	echo_subtask('Moving from build path to release path')

	run('mv %s %s' % (fetch('build_to'), fetch('release_to')))


def link_release_to_current():
	"""
	Creates current release symlink in `deploy_to` path
	"""

	ensure('release_to')
	ensure('current_path')

	echo_subtask("Linking release to current")

	release_to = fetch('release_to')

	with cd(release_to):
		run('ln -nfs %s %s' % (release_to, fetch('current_path')))


################################################################################
# Finallize deploy hooks
################################################################################

def cleanup_releases():
	"""
	Cleans up old releases
	"""

	ensure('releases_path')
	ensure('keep_releases')

	releases_count = str(fetch('keep_releases'))

	echo_subtask("Cleaning up old realeses. Keeping latest %s" % releases_count)

	with cd(fetch('releases_path')):
		cmd = '''
count=$(ls -A1 | sort -rn | wc -l)
remove=$((count > %s ? count - %s : 0))
ls -A1 | sort -rn | tail -n $remove | xargs rm -rf {}'''

		run(cmd % (releases_count, releases_count))


def remove_build_path():
	"""
	Removes a temporary build dir
	"""

	ensure('build_to')
	
	echo_subtask("Removing build path")

	with settings(hide('stdout', 'warnings'), warn_only=True):
		run('rm -rf %s' % fetch('build_to'))


def unlock():
	"""
	Forces a deploy unlock
	"""

	echo_subtask("Removing `deploy.lock` file")

	with cd(fetch('deploy_to')):
		run('rm -f deploy.lock')


################################################################################
# Rollback release
################################################################################


def rollback_release():
	"""
	Rollbacks the latest release.
	"""
	
	ensure('releases_path')
	ensure('current_path')

	releases_path = fetch('releases_path')

	with cd(releases_path):
		echo_subtask('Finding previous release for rollback')
		rollback_release = run('ls -1A | sort -n | tail -n 2 | head -n 1')

		if int(rollback_release) > 0:
			echo_subtask('Linking previous release to current')
			run('ln -nfs %s/%s %s' % (releases_path, rollback_release, fetch('current_path')))

			echo_subtask('Finding current release')
			current_release = run('ls -1A | sort -n | tail -n 1')

			if int(current_release) > 0:
				echo_subtask('Removing current release')
				run('rm -rf %s/%s' % (releases_path, current_release))
			else:
				abort('Can\'t find current release for remove.')
		else:
			abort('Can\'t find previous release for rollback.')


################################################################################
# Print
################################################################################


def get_error_states():
	def find_error_states(x):
		if x == 'success': return False
		return state.get(x) not in [True, None]

	return list(filter(find_error_states, state.keys()))


def print_verbose():
	print(yellow('\n=====> Verbose subtasks stats\n'))

	subtask_states = ['pre_deploy', 'deploy', 'post_deploy', 'finallize', 'on_success']

	for subtask_state_name in subtask_states:
		state_value = state.get(subtask_state_name)

		if state_value == None:
			print_value = white('not invoked')
		elif state_value == True:
			print_value = green('success')
		else:
			print_value = red('failed')

		print('%s - %s' % (yellow('* %s' % subtask_state_name), print_value))


def print_deploy_stats(task_name, start_time):
	if fetch('verbose') == True:
		print_verbose()

	error_states = get_error_states()

	if len(error_states) > 0:
		echo_task('Deploy errors', error=True)

		for error_state in error_states:
			echo_comment(('\n[ERROR]\n%s' % state.get(error_state)), error=True)

	if state.get('success') == True:
		print(yellow('\n-----> Release number: %s' % fetch('release_number')))

	print_stats_args = [task_name, start_time]
	if state.get('success') != True: print_stats_args.append(True)
	print_task_stats(*print_stats_args)
