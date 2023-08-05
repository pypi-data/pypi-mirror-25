# -*- coding: utf-8 -*-
import ntpath
import os

# @define_host('my_site@example.com')
from builtins import Exception

import fabtools
import yaml
from fabric.api import env
from fabric.context_managers import settings, hide, cd
from fabric.contrib.files import append, exists, sed
from fabric.decorators import task
from fabric.operations import run, sudo, put, local, prompt
from fabtools import vagrant, user
from fabtools.require import deb

updated = False

SERVERS_TO_RUN = []
APPS_INSTALL = []


def log(msg):
    msg = (('=' * 30) + ' {0} ' + ('=' * 30)).format(msg)
    print(msg)


def apt_get(package):
    global updated
    if not updated:
        updated = True
        log('UPDATING')
        with settings(hide('warnings', 'stdout'), warn_only=True):
            sudo('apt-get -y --no-upgrade update')

    log('INSTALLING PACKAGE {0}'.format(package))
    with settings(hide('warnings', 'stdout'), warn_only=True):
        with settings():
            deb.install(package)



def create_admin_account(admin, default_password=None):
    """Create an account for an admin to use to access the server."""
    env.user = "root"

    opts = dict(
        admin=admin,
        default_password=default_password or env.get('default_password') or 'secret',
    )

    # create user
    sudo('egrep %(admin)s /etc/passwd || adduser %(admin)s --disabled-password --gecos ""' % opts)

    # add public key for SSH access
    if not exists('/home/%(admin)s/.ssh' % opts):
        sudo('mkdir /home/%(admin)s/.ssh' % opts)

    opts['pub'] = prompt("Paste %(admin)s's public key: " % opts)
    sudo("echo '%(pub)s' > /home/%(admin)s/.ssh/authorized_keys" % opts)

    # allow this user in sshd_config
    append("/etc/ssh/sshd_config", 'AllowUsers %(admin)s@*' % opts, use_sudo=True)

    # allow sudo for maintenance user by adding it to 'sudo' group
    sudo('gpasswd -a %(admin)s sudo' % opts)

    # set default password for initial login
    sudo('echo "%(admin)s:%(default_password)s" | chpasswd' % opts)

def harden_sshd(allow_root_login, allow_password_auth):
    """Security harden sshd."""

    # Disable password authentication

    if allow_password_auth != None:
        sed('/etc/ssh/sshd_config',
            '#PasswordAuthentication yes',
            'PasswordAuthentication no',
            use_sudo=True)
    #
    # Deny root login
    if allow_root_login != None:
        sed('/etc/ssh/sshd_config',
            'PermitRootLogin yes',
            'PermitRootLogin no',
            use_sudo=True)

    fabtools.service.restart('ssh')
    # sudo("service ssh restart")

def set_system_time(timezone=None):
    """Set timezone and install ``ntp`` to keep time accurate."""

    opts = dict(
        timezone=timezone or env.get('timezone') or '/usr/share/zoneinfo/UTC',
    )

    # set timezone
    sudo('cp %(timezone)s /etc/localtime' % opts)

    # install NTP
    sudo('apt-get -yq install ntp')


def install_unattended_upgrades(email=None):
    """Configure Ubuntu to automatically install security updates."""
    opts = dict(
        email=email or env.get('email')
    )

    sudo('apt-get -yq install unattended-upgrades')
    sed('/etc/apt/apt.conf.d/50unattended-upgrades',
        '//Unattended-Upgrade::Mail "root@localhost";',
        'Unattended-Upgrade::Mail "%(email)s";' % opts,
        use_sudo=True)

    sed('/etc/apt/apt.conf.d/20auto-upgrades',
        'APT::Periodic::Update-Package-Lists "0";',
        'APT::Periodic::Update-Package-Lists "1";',
        use_sudo=True)

    append('/etc/apt/apt.conf.d/20auto-upgrades',
           'APT::Periodic::Unattended-Upgrade "1";',
           use_sudo=True)


def config_docker_ubuntu_xenial():
    """
    Install the docker on host
    :return:
    """

    sudo('apt-get update -y')
    apt_get('software-properties-common')
    apt_get('python-software-properties')
    sudo(
        'apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D')
    sudo("apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'")
    sudo('apt-get update -y')
    sudo('apt-cache policy docker-engine')
    sudo('apt-get install docker-engine -y')
    sudo('usermod -aG docker $(whoami)')
    sudo('gpasswd -a ${USER} docker')
    apt_get('python-setuptools')
    apt_get('python-pip')
    sudo('pip install docker-compose')

    # For connecting to a remote Docker instance over a socket, install socat on the remote, and put the following in your fabfile:
    # ref https://docker-fabric.readthedocs.io/en/stable/installation.html#installation
    apt_get('socat')


def create_usesr(users):


    for u in users or []:
        if not user.exists(u['name']):

            user.create(u['name'],
                        create_home=True,
                        password=u['password'],
                        group='sudo')

        # config visudo
        visudo = '''
           #!/bin/sh
           if [ -z "$1" ]; then
             echo "Starting up visudo with this script as first parameter"
             export EDITOR=$0 && sudo -E visudo
           else
             echo "Changing sudoers"
             echo "%s ALL=(ALL:ALL) ALL" >> $1
           fi ''' % (u['name'])

        VISUDO_FILENAME = '/tmp/visudo.sh'
        sudo('rm -rf {0}'.format(VISUDO_FILENAME))
        append(VISUDO_FILENAME, visudo, True)
        sudo('chmod +x %s' % VISUDO_FILENAME)
        sudo(VISUDO_FILENAME)

    # create directory(.ssh) if it does not exists
    if not exists('~/.ssh'):
        run('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
        

def config_nginx_app(appname, domain, port=80, config_nginx=None):

    if not config_nginx:
        config_nginx = '''
                    server {{
                            listen  80;
                            server_name {domain};                        
                            error_log  /var/log/nginx/%s-error.log  warn;
                            access_log /var/log/nginx/%s-access.log;
    
                            gzip on;
                            gzip_disable "msie6";
    
                            gzip_comp_level 6;
                            gzip_min_length 1100;
                            gzip_buffers 16 8k;
                            gzip_proxied any;
                            gzip_types
                                text/plain
                                text/css
                                text/js
                                text/xml
                                text/javascript
                                application/javascript
                                application/x-javascript
                                application/json
                                application/xml
                                application/xml+rss;
    
                            location / {{
                              sendfile off;
                              proxy_pass         http://127.0.0.1:{server_port};
                              proxy_redirect     default;
                              proxy_http_version 1.1;
                        
                              proxy_set_header   Host             $host;
                              proxy_set_header   X-Real-IP        $remote_addr;
                              proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
                              proxy_max_temp_file_size 0;

                                                            
                            }}
                    }}'''.format(domain=domain, server_port=port)

    default = '''                
                server {
                    return 404;
                }'''

    # nginx
    sites_available = "/etc/nginx/sites-available/{0}".format(appname)
    sites_enabled = "/etc/nginx/sites-enabled/{0}".format(appname)
    run("sudo rm -rf {0}".format(sites_available))
    run("sudo rm -rf {0}".format(sites_enabled))

    append(sites_available, config_nginx, use_sudo=True)

    # This removes the default configuration profile for Nginx
    sudo('rm -fv /etc/nginx/sites-enabled/default')
    append('/etc/nginx/sites-enabled/default', default, use_sudo=True)

    sudo(' ln -s %s %s' % (sites_available, sites_enabled))


    sudo('service nginx restart')


@task
def config_server(server_name):
    # Read the config file
    path = os.getcwd()+'/easydeploy.yml'
    with open(path, 'r') as f:
        config = yaml.load(f.read())

    for server_group in config.get('servers'):
        if server_group.get('name') == server_name:

            hosts = server_group.get('hosts')
            for host in hosts:

                log('HOST : ' + str(host))

                if server_group.get('vagrant'):
                    log('executando vagrant')
                    vagrant.vagrant()
                else:
                    env.host_string = host
                    env.user = server_group.get('user_access', 'root')

                log('Configurando servidor "{0}"...'.format(host))

                sudo('apt-get update -y')
                # sudo('apt-get upgrade -y')

                # Install nginx
                apt_get('nginx')


                # create users
                if server_group.get('users_create'):
                    create_usesr(server_group.get('users_create'))

                # Keep the server up to date
                # https://help.ubuntu.com/lts/serverguide/automatic-updates.html
                if server_group.get('email_for_security_updates'):
                    install_unattended_upgrades(server_group.get('email_for_security_updates'))


                # install packages
                for pkg in server_group.get('pkg') or []:
                    apt_get(pkg)

                # Change TIMEZONE
                if server_group.get('timezone'):
                    sudo('apt-get install language-pack-pt -y')
                    run("export TZ=\":{0}\"".format(server_group.get('timezone')))
                    run("date")

                # Security settings
                security = server_group.get('security')

                if security:

                    log('Security Settings')

                    if security.get('fail2ban'):
                        log('Configuring fail2ban')
                        apt_get('fail2ban')
                        sudo('service fail2ban restart')

                    harden_sshd(allow_root_login=security.get('allow_root_login'),
                                                allow_password_auth=security.get('allow_password_auth'))

                    # check if there is firewall settings
                    # by default, the UFW deny all outgoing traffic
                    firewall_config = security.get('firewall')

                    if firewall_config:

                        # Rules for incoming
                        for incoming in firewall_config.get('in') or []:
                            ports = incoming.get('port').split(',')
                            for port in ports:
                                sudo('ufw {2} in {0}/{1}'.format(port, incoming.get('protocol'), incoming.get('type')))

                        # Restart firewall to changes make effects
                        sudo('ufw --force enable')

                config_docker_ubuntu_xenial()


@task
def deploy(server_name='', app_name=''):

    # Read the config file
    path = os.getcwd() + '/easydeploy.yml'
    try:
        with open(path, 'r') as f:
            config = yaml.load(f.read())
    except:
        raise Exception('Config file not found in {0}'.format(path))

    for server_group in config.get('servers'):
        if server_group.get('name') == server_name:

            hosts = server_group.get('hosts')

            for host in hosts:

                log('HOST : ' + str(host))

                if server_group.get('vagrant'):
                    log('executando vagrant')
                    vagrant.vagrant()
                else:
                    env.host_string = host
                    env.user = server_group.get('user_access', 'root')

                # Check the app to install
                for app in config.get('apps'):
                    if app.get('name') == app_name:

                        # make sure the directory for app is there!
                        app_path = '/tmp/{0}/'.format(app_name)

                        run('rm -rf {0}'.format(app_path))

                        run('mkdir -p {0}'.format(app_path))

                        # Copy the docker-compose file
                        docker_compose_file = app.get('docker_compose') or 'docker-compose.yml'
                        put(docker_compose_file, app_path + '/docker-compose.yml')

                        # upload the files and docker-compose to the app directory in server
                        
                        filename = '/tmp/app.tar'

                        # with settings(hide('warnings', 'stdout'), warn_only=True):
                        #     local('rm -rf {0}'.format(filename))
                        if os.path.exists(filename):
                            os.remove(filename)

                        for file in app.get('upload') or []:
                            local('tar --append --file={filename} {file}'.format(filename=filename,file=file ))

                        if os.path.exists(filename):
                           put(filename, app_path)

                        with cd(app_path):
                            if os.path.exists(filename):
                                filename = ntpath.basename(filename)
                                run('tar -xvf {0} '.format(filename))

                            sudo('docker-compose stop')
                            sudo('docker-compose rm -f')
                            sudo('docker-compose up -d --build')

                        # Configure nginx to router app propertly
                        config_nginx_app(app_name, app.get('domain'), app.get('container_port') )



#
# if __name__ == '__main__':
#     config_server('SigeflexApi')

# if __name__ == '__main__':
#     config_server('linode')
#


# if __name__ == '__main__':
#     deploy('MyServerGroupName', 'mysql')

#
# if __name__ == '__main__':
#     deploy('SigeflexApi', 'zabbix')


    # if __name__ == '__main__':
    #     config_app('vagrant','sigeflex_frontend')
