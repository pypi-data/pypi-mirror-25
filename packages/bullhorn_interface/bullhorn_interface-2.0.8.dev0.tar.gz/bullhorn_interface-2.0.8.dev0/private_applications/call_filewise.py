import subprocess
import fire


def term_call(call_file="bullhorn/bullhorn_refresh.py", num_terms=5, num_calls=100):
    for i in range(num_terms):
        subprocess.Popen(['xterm', '-T', f"{i} {call_file}",
                          '-n', f"{i} {call_file}",
                          '-hold', '-e', 'python',
                          f'bullhorn/bullhorn_refresh.py',
                          f'--num_calls', f'{num_calls}',
                          f'--version', f'{i}'])

if __name__ == "__main__":
    fire.Fire(term_call)
