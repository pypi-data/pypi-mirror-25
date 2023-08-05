import pypandoc
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

package_name = "SSLProxies24"
package_version = "1.3.6"
setup(
    name=package_name,
    version=package_version,
    packages=[package_name],
    description='Obtenha e valide vários Proxys diariamente com este pacote. (Thread).',
    long_description=long_description,
    requires=["requests", "defusedxml"],
    python_requires='>=3.6',
    license='MIT',
    author="Henrique da Silva Santos (rique_dev)",
    author_email="rique_dev@hotmail.com",
    url="https://github.com/riquedev/SSLProxies24Feed",
    download_url='https://github.com/riquedev/SSLProxies24Feed/archive/master.zip',
    keywords=['proxy', 'ssl', '24', 'feed', 'blog', 'anonymous'],
    install_requires=["requests", "defusedxml"]
)
