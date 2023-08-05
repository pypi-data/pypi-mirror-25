import re
import signal
import errno
import sys
import os
import atexit
import pexpect
from subprocess import check_output
from ipykernel.kernelbase import Kernel

from . import utils

__version__ = '0.1.0'

version_pat = re.compile(r'Lua (\d+(\.\d+)+)')

logger = utils.make_logger('ILua', fname='ilua_kernel.log')

PY3 = (sys.version_info[0] >= 3)

if PY3:
    def u(s):
        return s
else:
    def u(s):
        if isinstance(s, str):
            return s.decode('utf-8')
        return s

PEXPECT_PROMPT = u('PEXPECT_PROMPT>')
PEXPECT_STDIN_PROMPT = u('PEXPECT_PROMPT+')
PEXPECT_CONTINUATION_PROMPT = u">> "

class LuaREPLWrapper(object):
    """
    A subclass of REPLWrapper specific for the Lua shell.
    run_command is the only method overridden.
    """
    def __init__(self, cmd_or_spawn, prompt_regex, prompt_change_cmd,
                 new_prompt_regex=PEXPECT_PROMPT,
                 continuation_prompt_regex=PEXPECT_CONTINUATION_PROMPT,
                 stdin_prompt_regex=PEXPECT_STDIN_PROMPT,
                 extra_init_cmd=None,
                 prompt_emit_cmd=None,
                 echo=True):

        if isinstance(cmd_or_spawn, str):
            self.child = pexpect.spawnu(cmd_or_spawn, echo=echo,
                                        codec_errors="ignore",
                                        encoding="utf-8")
        else:
            self.child = cmd_or_spawn

        if self.child.echo and not echo:
            # Existing spawn instance has echo enabled, disable it
            # to prevent our input from being repeated to output.
            self.child.setecho(False)
            self.child.waitnoecho()

        # Convert all arguments to unicode.
        prompt_regex = u(prompt_regex)
        prompt_change_cmd = u(prompt_change_cmd)
        continuation_prompt_regex = u(continuation_prompt_regex)
        stdin_prompt_regex = u(stdin_prompt_regex)
        prompt_emit_cmd = u(prompt_emit_cmd)

        self.echo = echo
        self.prompt_emit_cmd = prompt_emit_cmd

        if prompt_change_cmd is None:
            self.prompt_regex = u(prompt_regex)
        else:
            self.set_prompt(prompt_regex,
                            prompt_change_cmd.format(new_prompt_regex,
                                                     continuation_prompt_regex))
            self.prompt_regex = new_prompt_regex
        self.continuation_prompt_regex = continuation_prompt_regex
        self.stdin_prompt_regex = stdin_prompt_regex

        self._stream_handler = None
        self._stdin_handler = None
        self._expect_prompt()

        if extra_init_cmd is not None:
            self.run_command(extra_init_cmd)

        atexit.register(self.terminate)

        #self._expect_prompt()
        logger.info('Making LuaREPLWrapper')

    def sendline(self, line):
        self.child.sendline(u(line))
        if self.echo:
            self.child.readline()

    def set_prompt(self, prompt_regex, prompt_change_cmd):
        self.child.expect(prompt_regex)
        self.sendline(prompt_change_cmd)

    def _expect_prompt(self, timeout=None):
        """Expect a prompt from the child.
        """
        stream_handler = self._stream_handler
        stdin_handler = self._stdin_handler
        # logger.debug('-------_expect_prompt ---------')
        # logger.debug(self.prompt_regex)
        # logger.debug(self.continuation_prompt_regex)
        # logger.debug(self.stdin_prompt_regex)
        # logger.debug('----------------')
        expects = [self.prompt_regex, self.continuation_prompt_regex,
                   self.stdin_prompt_regex, 'u">> "']
        if stream_handler:
            expects += [u(self.child.crlf)]
        if self.prompt_emit_cmd:
            self.sendline(self.prompt_emit_cmd)
        while True:
            pos = self.child.expect(expects, timeout=timeout)
            if pos == 2 and stdin_handler:
                resp = stdin_handler(self.child.before + self.child.after)
                self.sendline(resp)
            elif pos == 3:  # End of line received
                stream_handler(self.child.before)
            else:
                if len(self.child.before) != 0 and stream_handler:
                    # prompt received, but partial line precedes it
                    stream_handler(self.child.before)
                break
        return pos

    def run_command(self, command, timeout=None, stream_handler=None,
                    stdin_handler=None):
        """Send a command to the REPL, wait for and return output.
        :param str command: The command to send. Trailing newlines are not needed.
          This should be a complete block of input that will trigger execution;
          if a continuation prompt is found after sending input, :exc:`ValueError`
          will be raised.
        :param int timeout: How long to wait for the next prompt. -1 means the
          default from the :class:`pexpect.spawn` object (default 30 seconds).
          None means to wait indefinitely.
        """
        # Split up multiline commands and feed them in bit-by-bit
        cmdlines = command.splitlines()
        # splitlines ignores trailing newlines - add it back in manually
        if command.endswith('\n'):
            cmdlines.append('')
        if not cmdlines:
            raise ValueError("No command was given")

        res = []
        self._stream_handler = stream_handler
        self._stdin_handler = stdin_handler
        self.sendline(cmdlines[0])
        for line in cmdlines[1:]:
            self._expect_prompt(timeout=timeout)
            res.append(self.child.before)
            self.sendline(line)

        # Command was fully submitted, now wait for the next prompt
        if self._expect_prompt(timeout=timeout) == 1:
            # We got the continuation prompt - command was incomplete
            self.interrupt()
            raise ValueError("Continuation prompt found - input was incomplete:\n" + command)
        return u''.join(res + [self.child.before])

    def interrupt(self):
        """Interrupt the process and wait for a prompt.
        Returns
        -------
        The value up to the prompt.
        """
        if pexpect.pty:
            self.child.sendintr()
        else:
            self.child.kill(signal.SIGINT)
        while 1:
            try:
                self._expect_prompt(timeout=-1)
                break
            except KeyboardInterrupt:
                pass
        return self.child.before

    def terminate(self):
        if pexpect.pty:
            self.child.close()
            return self.child.terminate()
        try:
            self.child.kill(signal.SIGTERM)
        except Exception as e:
            if e.errno != errno.EACCES:
                raise

class LuaKernel(Kernel):
    implementation = 'lua_kernel'
    implementation_version = __version__

    @property
    def language_version(self):
        #m = version_pat.search(self.banner)
        #return m.group(1)
        return '1.5.1'

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(['lua', '-v']).decode('utf-8')
        return self._banner

    language_info = {'name': 'lua',
                     'codemirror_mode': 'lua',
                     'mimetype': 'text/x-lua',
                     'file_extension': '.lua'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        logger.debug(self.language_info)
        logger.debug(self.language_version)
        logger.debug(self.banner)
        self._start_lua()

    def _start_lua(self):
        """Spwans `lua` subprocess"""
        try:
            self.luawrapper = LuaREPLWrapper("lua -i", u"> ", None, u"> ")
        finally:
            # Signal handlers are inherited by forked processes, and we can't easily
            # reset it from the subprocess. Since kernelapp ignores SIGINT except in
            # message handlers, we need to temporarily reset the SIGINT handler here
            # so that bash and its children are interruptible.
            sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        if not code.strip():
            logger.debug('Code.strip: {}'.format(code.strip()))
            return {'status': 'ok',
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {}}
        interrupted = False
        error = None
        try:
            logger.debug('---- Code ------')
            logger.debug(code)
            #output = self.luawrapper.run_command(code.rstrip())
            output = self.luawrapper.run_command(code, timeout=-1)
            logger.debug('---- Output ------')
            logger.debug(output)
            logger.debug('----------')
        except KeyboardInterrupt:
            self.luawrapper.child.sendeof()
            interrupted = True
            output = None
            error = 'KeyboardInterrupt.'
            self._start_lua()
        except (EOF, ValueError, RuntimeError) as e:
            output = None
            error = e.args[0]
            self._start_lua()
        finally:
            if error:
                error_msg = {'name': 'stderr', 'text': error + '\nRestarting lua...'}
                self.send_response(self.iopub_socket, 'stream', error_msg)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        if not silent and output:
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return_msg = {'status': 'ok', 'execution_count': self.execution_count,
                      'payload': [], 'user_expressions': {}}
        logger.debug('Return message: {}'.format(return_msg))
        return return_msg
