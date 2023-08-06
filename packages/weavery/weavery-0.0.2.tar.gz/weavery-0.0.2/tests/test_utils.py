from fabric.state import env
from dockerman import container
from syn.base_utils import assign, setitem
from envassert import group, user, file, detect

from weavery import groups, users, success, success_sudo,\
    ensure_group, ensure_user, ensure_file, ensure_absent,\
    start_service, apt_install, pip_install

PASSWORD = '$6$KvP9PaWo.8UGts2t$xraIE4zQ2gU2NfahGEdKT8S4MQF6V7u684nRpEZM/2.tK.2PY2tGZSY3YEPhPKAU/HFadJdMigOmfVWkvXJ3X/' # 'password'

#-------------------------------------------------------------------------------

def test1():
    with container('rastasheep/ubuntu-sshd') as c:
        with assign(env, 'host_string', c.status.ip_addr):
            with assign(env, 'user', 'root'):
                with assign(env, 'password', 'root'):
                    c.poll(22, timeout=10)

                    # success / success_sudo
                    assert success('true')
                    assert success_sudo('true')
                    assert not success('false')
                    assert not success_sudo('false')
                
                    # ensure_group
                    groupname = 'foogroup'
                    assert not group.is_exists(groupname)
                    assert groupname not in groups()
                    
                    ensure_group(groupname)
                    assert group.is_exists(groupname)
                    assert groupname in groups()

                    ensure_group(groupname)
                    assert group.is_exists(groupname)
                    
                    # ensure_user
                    username = 'foouser'
                    assert not user.exists(username)
                    assert username not in users()

                    ensure_user(username, PASSWORD, 'adm,sudo')
                    assert user.exists(username)
                    assert username in users()

                    assert user.is_belonging_group(username, username)
                    assert user.is_belonging_group(username, 'adm')
                    assert user.is_belonging_group(username, 'sudo')
                    assert not user.is_belonging_group(username, 'root')

                    ensure_user(username, PASSWORD, 'adm,sudo')
                    assert user.exists(username)

                    # ensure_file
                    dpath = '/foo/bar'
                    fpath = '/foo/bar/baz'

                    # Because envassert is bugged
                    with setitem(env, 'platform_family', detect.detect()):
                        assert not file.dir_exists(dpath)
                        ensure_file(dpath, '750', username, dir=True)
                        assert file.dir_exists(dpath)
                        assert file.owner_is(dpath, username)
                        assert file.group_is(dpath, username)
                        assert file.mode_is(dpath, '750')

                        assert not file.exists(fpath)
                        ensure_file(fpath, '640', username, group='adm')
                        assert file.is_file(fpath)
                        assert file.owner_is(fpath, username)
                        assert file.group_is(fpath, 'adm')
                        assert file.mode_is(fpath, '640')
                        
                        ensure_absent(fpath)
                        assert not file.exists(fpath)

                        ensure_absent(dpath, dir=True)
                        assert not file.dir_exists(dpath)
                    
                    # Services
                    start_service('ssh')
                    
                    # Packages
                    assert not success('which pip')
                    apt_install(['python-pip'], update=True)
                    assert success('which pip')

                    assert not success('python -c "import fmap"')
                    pip_install(['fmap'])
                    assert success('python -c "import fmap"')
                    
#-------------------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    from syn.base_utils import run_all_tests
    run_all_tests(globals(), verbose=True, print_errors=False)
