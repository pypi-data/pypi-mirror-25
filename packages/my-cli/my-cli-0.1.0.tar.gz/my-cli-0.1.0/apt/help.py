from subprocess import run, PIPE

INSTALL_CMD = r"""@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"""""


def has_choco():
    s = run(['choco'], shell=True, stdout=PIPE)
    return 'Chocolatey' in s.stdout.decode(encoding='UTF-8')


def install_choco():
    s = run(INSTALL_CMD, shell=True, stdout=PIPE)
    assert (s.returncode is 0)


def choco_run(args):
    run(['choco'] + args, shell=True)


def init():
    if not has_choco():
        install_choco()
