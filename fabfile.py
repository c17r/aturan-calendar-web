from datetime import datetime
from fabric.api import task, env, settings, cd, sudo, run, local, put, path, shell_env

server_user = 'aturan_calendar'
site_name = 'kkc'

stamp = datetime.now().strftime("v%Y%m%d%H%M%S")
stamptar = server_user + "-web-" + stamp + ".tar"
stampzip = stamptar + ".gz"

env.stamp = stamp
env.stamptar = stamptar
env.stampzip = stampzip
env.nginx = "/usr/sbin/nginx"
env.supervisor = "/usr/bin/supervisorctl"
env.server_user = server_user
env.site_name = site_name

@task
def live():
    env.env = "live"
    env.hosts = [
        "crow.endrun.org"
    ]

@task
def deploy():
    local('find . \( -name "*.pyc" -or -name "*.pyo" -or -name "*py.class" \) -delete')

    local("tar cf %(stamptar)s static/" % env)
    local("tar rf %(stamptar)s templates/" % env)
    local("tar rf %(stamptar)s application.py" % env)
    local("tar rf %(stamptar)s converters.py" % env)
    local("tar rf %(stamptar)s requirements.deploy" % env)
    local("tar rf %(stamptar)s requirements.lock" % env)
    local("tar rf %(stamptar)s gunicorn.conf.py" % env)

    local("gzip %(stamptar)s" % env)

    put(stampzip, "/tmp/%(stampzip)s" % env)

    local("rm %(stampzip)s" % env)

    with settings(sudo_user=server_user):

        with cd("/home/%(server_user)s/web" % env):
            sudo("mkdir -p %(stamp)s/src" % env)
            sudo("mkdir -p %(stamp)s/venv" % env)

        with cd("/home/%(server_user)s/web/%(stamp)s/" % env):
            sudo("tar xfz /tmp/%(stampzip)s -C ./src/" % env)

            with shell_env(PATH='/opt/pyenv/bin/:$PATH', PYENV_ROOT='/opt/pyenv'):
                sudo("virtualenv venv -p $(pyenv prefix 3.5.1)/bin/python")

            with path("./venv/bin", behavior="prepend"):
                sudo("pip install --quiet --no-cache-dir -r ./src/requirements.deploy")

        with cd("/home/%(server_user)s/web" % env):
            sudo("ln -nsf $(basename $(readlink -f current)) previous")
            sudo("ln -nsf %(stamp)s current" % env)

    sudo("%(supervisor)s restart aturan-calendar-web" % env)
    sudo("%(nginx)s -s reload" % env)

    sudo("rm /tmp/%(server_user)s*.tar.gz" % env)
