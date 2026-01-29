"""
Claude Socket Plugin for PyMOL

Headless socket listener that receives Python commands from Claude Code.
Auto-starts on load, no UI required.

Usage:
    run /path/to/claude_socket_plugin.py    # Start listening
    claude_status                            # Check connection status
    claude_stop                              # Stop listener
    claude_start                             # Restart listener
"""

import socket
import json
import threading
import traceback
import io
from contextlib import redirect_stdout

from pymol import cmd

# Global state
_server = None
_port = 9880


class SocketServer:
    def __init__(self, host='localhost', port=9880):
        self.host = host
        self.port = port
        self.socket = None
        self.client = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return False
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        return True

    def _run_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.socket.settimeout(1.0)

            print(f"Claude socket listener active on port {self.port}")

            while self.running:
                try:
                    new_client, address = self.socket.accept()
                    if self.client:
                        try:
                            self.client.close()
                        except:
                            pass
                    self.client = new_client
                    self.client.settimeout(1.0)
                    self._handle_client(address)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Connection error: {e}")
        except Exception as e:
            print(f"Socket server error: {e}")
            traceback.print_exc()
        finally:
            self._cleanup()

    def _handle_client(self, address):
        buffer = b''
        while self.running and self.client:
            try:
                data = self.client.recv(4096)
                if not data:
                    break
                buffer += data
                try:
                    command = json.loads(buffer.decode('utf-8'))
                    buffer = b''
                    result = self._execute_command(command)
                    response = json.dumps(result)
                    self.client.sendall(response.encode('utf-8'))
                except json.JSONDecodeError:
                    continue
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Client error: {e}")
                break
        if self.client:
            try:
                self.client.close()
            except:
                pass
            self.client = None

    def _execute_command(self, command):
        code = command.get("code", "")
        if not code:
            return {"status": "error", "error": "No code provided"}
        try:
            exec_globals = {"cmd": cmd, "__builtins__": __builtins__}
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(code, exec_globals)
            output = output_buffer.getvalue()
            if '_result' in exec_globals:
                output = str(exec_globals['_result'])
            return {"status": "success", "output": output or "OK"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _cleanup(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.client = None
        self.running = False

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(2.0)
        self._cleanup()

    @property
    def is_running(self):
        return self.running and self.thread and self.thread.is_alive()


def claude_status():
    """Print Claude socket listener status."""
    global _server
    if _server and _server.is_running:
        connected = "connected" if _server.client else "waiting"
        print(f"Claude socket listener: running on port {_port} ({connected})")
    else:
        print("Claude socket listener: not running")


def claude_stop():
    """Stop the Claude socket listener."""
    global _server
    if _server:
        _server.stop()
        _server = None
        print("Claude socket listener stopped")
    else:
        print("Claude socket listener was not running")


def claude_start(port=9880):
    """Start the Claude socket listener."""
    global _server, _port
    if _server and _server.is_running:
        print(f"Claude socket listener already running on port {_port}")
        return
    _port = port
    _server = SocketServer(port=port)
    _server.start()


# Register commands with PyMOL
cmd.extend("claude_status", claude_status)
cmd.extend("claude_stop", claude_stop)
cmd.extend("claude_start", claude_start)

# Auto-start on load
claude_start()
