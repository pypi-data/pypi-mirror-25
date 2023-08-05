# ebuild-daemon.bash; core ebuild processor handling code
# Copyright 2004-2012 Brian Harring <ferringb@gmail.com>
# License: BSD/GPL2

# These are functions that shouldn't be marked readonly, since they're runtime
# switchable.
PKGCORE_RUNTIME_FUNCS=( '__timed_call' )

__set_perf_debug() {
	if [[ ${PKGCORE_DEBUG} -ge 4 || -n ${PKGCORE_PERF_DEBUG} ]]; then
		__timed_call() {
			echo "timing $*" >&2
			time "$@"
			local __ret=$?
			echo "timed  $*" >&2
			return ${__ret}
		}
	else
		__timed_call() {
			"$@"
		}
	fi
}

__set_perf_debug

die() {
	# Temporary function used by the daemon, till proper die implementation is loaded.
	echo "$@" >&2
	exit 1
}

PKGCORE_EBD_PID=${BASHPID}
# Use ebd_read/ebd_write for talking to the running pkgcore instance instead of
# echo'ing to the fd yourself. This allows us to move the open fd's w/out
# issues down the line.
__ebd_read_line_nonfatal() {
	read -u ${PKGCORE_EBD_READ_FD} $1
}

__ebd_read_line() {
	__ebd_read_line_nonfatal "$@"
	local ret=$?
	[[ ${ret} -ne 0 ]] && \
		die "coms error in ${PKGCORE_EBD_PID}, read_line $@ failed w/ ${ret}: backing out of daemon."
}

# are we running a version of bash (4.1 or so) that does -N?
if echo 'y' | read -N 1 &> /dev/null; then
	__ebd_read_size()
	{
		read -u ${PKGCORE_EBD_READ_FD} -r -N $1 $2
		local ret=$?
		[[ ${ret} -ne 0 ]] && \
			die "coms error in ${PKGCORE_EBD_PID}, read_size $@ failed w/ ${ret}: backing out of daemon."
	}
else
	# fallback to a *icky icky* but working alternative.
	__ebd_read_size() {
		eval "${2}=\$(dd bs=1 count=$1 <&${PKGCORE_EBD_READ_FD} 2> /dev/null)"
		local ret=$?
		[[ ${ret} -ne 0 ]] && \
			die "coms error in ${PKGCORE_EBD_PID}, read_size $@ failed w/ ${ret}: backing out of daemon."
	}
fi

__ebd_read_cat_size() {
	dd bs=$1 count=1 <&${PKGCORE_EBD_READ_FD}
}

__ebd_write_line() {
	echo "$*" >&${PKGCORE_EBD_WRITE_FD}
	local ret=$?
	[[ ${ret} -ne 0 ]] && \
		die "coms error, write failed w/ ${ret}: backing out of daemon."
}

__ebd_write_raw() {
	echo -n "$*" >&${PKGCORE_EBD_WRITE_FD} || die "coms error, __ebd_write_raw failed;  Backing out."
}

for x in ebd_read_{line,{cat_,}size} __ebd_write_line __set_perf_debug; do
	declare -rf ${x}
done
unset -v x
declare -r PKGCORE_EBD_WRITE_FD PKGCORE_EBD_READ_FD

__ebd_sigint_handler() {
	EBD_DISABLE_DIEFUNC="yes"
	# silence ourselves as everything shuts down.
	exec 2>/dev/null
	exec 1>/dev/null
	# suppress sigpipe; if we can't tell the parent to die,
	# it's already shutting us down.
	trap "exit 2" SIGPIPE
	__ebd_write_line "killed"
	trap - SIGINT
	# this relies on the python side to *not* discard the killed
	exit 2
}

__ebd_sigkill_handler() {
	EBD_DISABLE_DIEFUNC="yes"
	# silence ourselves as everything shuts down.
	exec 2>/dev/null
	exec 1>/dev/null
	# suppress sigpipe; if we can't tell the parent to die,
	# it's already shutting us down.
	trap "exit 9" SIGPIPE
	__ebd_write_line "killed"
	trap - SIGKILL
	exit 9
}

__ebd_exec_main() {
	# ensure the other side is still there.  Well, this moreso is for the python side to ensure
	# loading up the intermediate funcs succeeded.
	local com
	__ebd_read_line com
	if [[ ${com} != "dude?" ]]; then
		echo "serv init coms failed, received ${com} when expecting 'dude?'" >&2
		exit 1
	fi
	__ebd_write_line "dude!"
	__ebd_read_line PKGCORE_EBD_PATH
	[[ -z ${PKGCORE_EBD_PATH} ]] && { __ebd_write_line "empty PKGCORE_EBD_PATH;"; exit 1; }

	# get our die functionality now.
	if ! source "${PKGCORE_EBD_PATH}"/exit-handling.lib; then
		__ebd_write_line "failed sourcing exit handling functionality"
		exit 2
	fi

	if ! source "${PKGCORE_EBD_PATH}"/isolated-functions.lib; then
		__ebd_write_line "failed sourcing isolated-functions.lib"
		exit 2
	fi

	__ebd_read_line PKGCORE_PYTHON_BINARY
	[[ -z ${PKGCORE_PYTHON_BINARY} ]] && die "empty PKGCORE_PYTHON_BINARY, bailing"
	__ebd_read_line PKGCORE_PYTHONPATH
	[[ -z ${PKGCORE_PYTHONPATH} ]] && die "empty PKGCORE_PYTHONPATH, bailing"

	if ! source "${PKGCORE_EBD_PATH}"/ebuild.lib >&2; then
		__ebd_write_line "failed"
		die "failed sourcing ${PKGCORE_EBD_PATH}/ebuild.lib"
	fi

	__ebd_read_line com
	case ${com} in
		"sandbox_log?")
			if [[ ! ${SANDBOX_LOG} ]]; then
				echo "sandbox enabled but no SANDBOX_LOG?!"
				exit 1
			fi
			__ebd_write_line "${SANDBOX_LOG}"
			declare -rx SANDBOX_LOG=${SANDBOX_LOG}
			addwrite "${SANDBOX_LOG}"
			;;
		no_sandbox)
			;;
		*)
			echo "unknown com '${com}'"
			exit 1
			;;
	esac

	__IFS_push $'\n'
	readonly_vars=( $(readonly) )
	__IFS_pop
	# extract variable names from declarations
	readonly_vars=( "${readonly_vars[@]/%=*/}" )
	readonly_vars=( "${readonly_vars[@]/#* * /}" )

	for x in "${readonly_vars[@]}"; do
		if ! __safe_has "${x}" "${PKGCORE_BLACKLIST_VARS[@]}"; then
			PKGCORE_BLACKLIST_VARS+=( ${x} )
		fi
	done
	__ebd_write_line ${readonly_vars[@]}
	unset -v x readonly_vars

	# protect ourselves
	declare -rx PKGCORE_EBD_PATH=${PKGCORE_EBD_PATH}
	declare -rx PKGCORE_PYTHON_BINARY=${PKGCORE_PYTHON_BINARY}
	declare -rx PKGCORE_PYTHONPATH=${PKGCORE_PYTHONPATH}

	# export env path for helpers
	declare -x PKGCORE_EBD_ENV

	if ! source "${PKGCORE_EBD_PATH}"/ebuild-daemon.lib >&2; then
		__ebd_write_line "failed"
		die "failed sourcing ${PKGCORE_EBD_PATH}/ebuild-daemon.lib"
	fi

	__colored_output_disable
	declare -A PKGCORE_PRELOADED_ECLASSES

	trap __ebd_sigint_handler SIGINT
	trap __ebd_sigkill_handler SIGKILL

	# finally, load the master list of pkgcore funcs. fallback to
	# regenerating it if needed.
	if [[ -e ${PKGCORE_EBD_PATH}/funcnames/global ]]; then
		PKGCORE_BLACKLIST_FUNCS+=( $(<"${PKGCORE_EBD_PATH}"/funcnames/global) )
	else
		PKGCORE_BLACKLIST_FUNCS+=( $("${PKGCORE_EBD_PATH}"/generate_global_func_list.bash 2> /dev/null) )
	fi
	[[ $? -eq 0 ]] || die "failed reading the global function skip list"

	for x in "${PKGCORE_BLACKLIST_FUNCS[@]}"; do
		__is_function "${x}" || continue
		if ! __safe_has "${x}" "${PKGCORE_RUNTIME_FUNCS[@]}"; then
			declare -fr ${x} &> /dev/null
		fi
	done
	unset -v x

	source "${PKGCORE_EBD_PATH}"/eapi/depend.lib >&2 || die "failed sourcing eapi/depend.lib"
	__ebd_main_loop
	exit 0
}

__ebd_process_sandbox_results() {
	if [[ -z ${SANDBOX_LOG} || ! -e ${SANDBOX_LOG} ]]; then
		return 0;
	fi
	echo "sandbox exists- ${SANDBOX_LOG}" >&2
	__request_sandbox_summary >&2
	echo "SANDBOX_ON:=${SANDBOX_ON:-unset}" >&2
	echo "SANDBOX_DISABLED:=${SANDBOX_DISABLED:-unset}" >&2
	echo "SANDBOX_READ:=${SANDBOX_READ:-unset}" >&2
	echo "SANDBOX_WRITE:=${SANDBOX_WRITE:-unset}" >&2
	echo "SANDBOX_PREDICT:=${SANDBOX_PREDICT:-unset}" >&2
	echo "SANDBOX_DEBUG:=${SANDBOX_DEBUG:-unset}" >&2
	echo "SANDBOX_DEBUG_LOG:=${SANDBOX_DEBUG_LOG:-unset}" >&2
	echo "SANDBOX_LOG:=${SANDBOX_LOG:-unset}" >&2
	echo "SANDBOX_ARMED:=${SANDBOX_ARMED:-unset}" >&2
	return 1
}

__ebd_process_ebuild_phases() {
	# note that this is entirely subshelled; as such exit is used rather than returns
	(
	declare -r PKGCORE_QA_SUPPRESSED=false
	local phases=$@
	local is_depends=true
	if [[ ${phases/depend} == ${phases} ]]; then
		is_depends=false
	fi
	local cont=0

	while [[ ${cont} == 0 ]]; do
		local line=''
		__ebd_read_line line
		case ${line} in
			start_receiving_env*)
				line=${line#start_receiving_env }
				case ${line} in
					file*)
						line=${line#file }
						PKGCORE_EBD_ENV=${line}
						source "${PKGCORE_EBD_ENV}"
						cont=$?
						;;
					bytes*)
						line=${line#bytes }
						__ebd_read_size "${line}" line
						__IFS_push $'\0'
						eval "${line}"
						cont=$?
						__IFS_pop
						;;
					lines|*)
						while __ebd_read_line line && [[ ${line} != "end_receiving_env" ]]; do
							__IFS_push $'\0'
							eval "${line}"
							cont=$?
							__IFS_pop
							if [[ ${cont} != 0 ]]; then
								echo "err, env receiving threw an error for '${line}': $?" >&2
								break
							fi
						done
						;;
				esac
				if [[ ${cont} != 0 ]]; then
					__ebd_write_line "env_receiving_failed"
					exit 1
				fi
				__set_perf_debug
				__ebd_write_line "env_received"
				;;
			logging*)
				PORTAGE_LOGFILE=${line#logging }
				__ebd_write_line "logging_ack"
				;;
			set_sandbox_state*)
				if [[ $(( ${line:18} )) -eq 0 ]]; then
					export SANDBOX_DISABLED=1
				else
					export SANDBOX_DISABLED=0
					export SANDBOX_VERBOSE="no"
				fi
				;;
			start_processing)
				if ${is_depends} && [[ -n ${PKGCORE_METADATA_PATH} ]]; then
					export PATH=${PKGCORE_METADATA_PATH}
				fi
				cont=2
				;;
			shutdown_daemon)
				break
				;;
			alive)
				__ebd_write_line "yep!"
				;;
			*)
				echo "received unknown com during phase processing: ${line}" >&2
				exit 1
				;;
		esac
	done
	if [[ ${cont} != 2 ]]; then
		exit ${cont}
	fi

	[[ -n ${PORTAGE_LOGFILE} ]] && addwrite "$(readlink -f "${PORTAGE_LOGFILE}")"

	[[ -z ${PKGCORE_NOCOLOR} ]] && __colored_output_enable

	[[ -n ${PORTAGE_TMPDIR} ]] && {
		addpredict "${PORTAGE_TMPDIR}"
		addwrite "${PORTAGE_TMPDIR}"
		addread "${PORTAGE_TMPDIR}"
	}

	local ret
	umask 0022

	if [[ -z ${PORTAGE_LOGFILE} ]]; then
		__execute_phases ${phases}
		ret=$?
	else
		__execute_phases ${phases} &> >(umask 0002; tee -i -a "${PORTAGE_LOGFILE}")
		ret=$?
	fi

	if [[ ${ret} -ne 0 ]]; then
		__ebd_process_sandbox_results
		exit ${ret}
	fi
	exit 0
	)
}

__ebd_process_metadata() {
	# protect the env.
	# note the local usage is redundant in light of it, but prefer to write it this
	# way so that if someone ever drops the (), it'll still not bleed out.
	(
		# Heavy QA checks (IFS, shopt, etc) are suppressed for speed
		declare -r PKGCORE_QA_SUPPRESSED=false
		# Wipe __mode; it bleeds from our parent.
		unset -v __mode
		local __data
		local __ret
		__ebd_read_size "$1" __data
		local IFS=$'\0'
		eval "$__data"
		__ret=$?
		unset -v __data
		[[ ${__ret} -ne 0 ]] && exit 1
		unset -v __ret
		local IFS=$' \t\n'

		if [[ -n ${PKGCORE_METADATA_PATH} ]]; then
			export PATH=${PKGCORE_METADATA_PATH}
		fi

		# invoked internally by bash on PATH search failure, see the bash man
		# page section on command execution for details
		command_not_found_handle() {
			die "External commands disallowed during metadata regen: ${*}"
		}

		PKGCORE_SANDBOX_PID=${PPID}
		__execute_phases "${2:-depend}" && exit 0
		__ebd_process_sandbox_results
		exit 1
	)
}

__make_preloaded_eclass_func() {
	eval "__preloaded_eclass_$1() {
		$2
	}"
	PKGCORE_PRELOADED_ECLASSES[$1]=__preloaded_eclass_$1
}

__ebd_main_loop() {
	PKGCORE_BLACKLIST_VARS+=( __mode com is_depends phases line cont )
	SANDBOX_ON=1
	while :; do
		local com=''
		# If we don't manage to read, this means that the other end hung up.
		# exit.
		__ebd_read_line_nonfatal com || com="shutdown_daemon"
		case ${com} in
			process_ebuild*)
				# cleanse whitespace.
				local phases=$(echo ${com#process_ebuild})
				PKGCORE_SANDBOX_PID=${PPID}
				__ebd_process_ebuild_phases ${phases}
				# tell python if it succeeded or not.
				if [[ $? -ne 0 ]]; then
					__ebd_write_line "phases failed"
				else
					__ebd_write_line "phases succeeded"
				fi
				;;
			shutdown_daemon)
				break
				;;
			preload_eclass\ *)
				success="succeeded"
				com=${com#preload_eclass }
				for e in ${com}; do
					x=${e##*/}
					x=${x%.eclass}
					if ! $(type -P bash) -n "${e}"; then
						echo "errors detected in '${e}'" >&2
						success='failed'
						break
					fi
					__make_preloaded_eclass_func "${x}" "$(< "${e}")"
				done
				__ebd_write_line "preload_eclass ${success}"
				unset -v e x success
				;;
			clear_preloaded_eclasses)
				unset -v PKGCORE_PRELOADED_ECLASSES
				declare -A PKGCORE_PRELOADED_ECLASSES
				__ebd_write_line "clear_preloaded_eclasses succeeded"
				;;
			set_metadata_path\ *)
				line=${com#set_metadata_path }
				__ebd_read_size "${line}" PKGCORE_METADATA_PATH
				__ebd_write_line "metadata_path_received"
				;;
			gen_metadata\ *|gen_ebuild_env\ *)
				local __mode="depend"
				[[ ${com} == gen_ebuild_env* ]] && __mode="generate_env"
				line=${com#* }
				if __ebd_process_metadata "${line}" "${__mode}"; then
					__ebd_write_line "phases succeeded"
				else
					__ebd_write_line "phases failed"
				fi
				;;
			alive)
				__ebd_write_line "yep!"
				;;
			*)
				echo "received unknown com: ${com}" >&2
				exit 1
				;;
		esac
	done
}

# start the daemon if requested
[[ $1 == "daemonize" ]] && __ebd_exec_main

:
