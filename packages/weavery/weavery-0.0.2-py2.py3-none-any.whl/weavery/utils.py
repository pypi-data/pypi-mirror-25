from fabric.api import run, sudo, settings, hide

#-------------------------------------------------------------------------------
# Utilities

def groups():
    out = sudo('cut -d: -f1 /etc/group')
    return out.split()

def users():
    out = sudo('cut -d: -f1 /etc/passwd')
    return out.split()

def success(cmd):
    with settings(warn_only=True):
        with hide('everything'):
            out = run(cmd)
            return not bool(out.return_code)

def success_sudo(cmd):
    with settings(warn_only=True):
        with hide('everything'):
            out = sudo(cmd)
            return not bool(out.return_code)

#-------------------------------------------------------------------------------
# Tasks

# TODO: accept single string without error
def apt_install(pkgs, update=False):
    if update:
        sudo('apt-get update')
    pstr = ' '.join(pkgs)
    sudo('apt-get install -y {}'.format(pstr))

# TODO: accept single string without error
def pip_install(pkgs):
    pstr = ' '.join(pkgs)
    sudo('pip install -U {}'.format(pstr))

def create_group(grp):
    sudo('groupadd {}'.format(grp))
    
def ensure_group(grp):
    if grp not in groups():
        create_group(grp)

# TODO: needs to ensure that user is a member of the groups in question
# TODO: needs to ensure the existence of each group in question
def create_user(usr, passwd, groups):
    ensure_group(usr)
    return success_sudo("useradd -m -g {} -G {} -p '{}' "
                        "-s /bin/bash {}"
                        .format(usr, groups, passwd, usr))

def ensure_user(usr, passwd, groups):
    if usr not in users():
        return create_user(usr, passwd, groups)

def ensure_file(path, perm, owner, group=None, dir=False):
    if group is None:
        group = owner

    success = False
    if not success_sudo('ls {}'.format(path)):
        if dir:
            sudo('mkdir -p {}'.format(path))
        else:
            sudo('touch {}'.format(path))
        success = True

    sudo('chown {}:{} {}'.format(owner, group, path))
    sudo('chmod {} {}'.format(perm, path))
    return success

def ensure_absent(path, dir=False):
    if success_sudo('ls {}'.format(path)):
        if dir:
            sudo('rm -rf {}'.format(path))
        else:
            sudo('rm -f {}'.format(path))

def start_service(svc):
    sudo('service {} start'.format(svc))

#-------------------------------------------------------------------------------
