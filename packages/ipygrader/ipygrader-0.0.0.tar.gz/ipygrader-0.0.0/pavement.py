"""paver config file"""

# from testing python book
from paver.easy import sh
from paver.tasks import task, needs




@task
def pypi():
    """Instalation on PyPi"""
    sh('python setup.py sdist')
    sh('twine upload dist/*')

@task
def local():
    """local install"""
    sh("pip uninstall ipygrader")
    sh("python setup.py install develop")



@task
def default():
    """Tests"""
    sh("python ipygrader/ipygrader.py demo_python_TEACHER.ipynb demo_python_STUDENT.ipynb")
    sh("python nbgrade.py demo_python_TEACHER.ipynb demo_python_SOLUTION.ipynb")

    sh("python ipygrader/ipygrader.py demo_R_TEACHER.ipynb demo_R_STUDENT.ipynb")
    sh("python nbgrade.py demo_R_TEACHER.ipynb demo_R_SOLUTION.ipynb")
