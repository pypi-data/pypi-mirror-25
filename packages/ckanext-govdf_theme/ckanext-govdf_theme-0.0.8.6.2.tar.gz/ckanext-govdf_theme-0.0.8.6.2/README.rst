.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/"lucasjlma"/ckanext-govdf_theme.svg?branch=master
    :target: https://travis-ci.org/"lucasjlma"/ckanext-govdf_theme

.. image:: https://coveralls.io/repos/"lucasjlma"/ckanext-govdf_theme/badge.svg
  :target: https://coveralls.io/r/"lucasjlma"/ckanext-govdf_theme

.. image:: https://pypip.in/download/ckanext-govdf_theme/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-govdf_theme/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-govdf_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-govdf_theme/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-govdf_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-govdf_theme/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-govdf_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-govdf_theme/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-govdf_theme/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-govdf_theme/
    :alt: License

===================================================
Template CKAN para PDA do GDF - ckanext-govdf_theme
===================================================

.. Coloque uma descrição da sua extensão aqui:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!

Para ter acesso á área de usuário é necessário digitar ``/user/login`` depois do endereço url base.

     http://dadosabertos.df.gov.br/user/login


----------
Instalação
----------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

Para instalar ckanext-govdf_theme:

1. Ative seu ambiente virtual CKAN, por exemplo::

     . /usr/lib/ckan/default/bin/activate

2. Instale o pacote Python ckanext-govdf_theme no seu ambiente virtual::

     pip install ckanext-govdf_theme

3. Adicione ``govdf_theme`` na área ``ckan.plugins`` no seu arquivo de configurações do CKAN (por padrão o arquivo de configurações está em
   ``/etc/ckan/default/production.ini``).

4. Reinicia o CKAN. Por exemplo se o CKAN foi implantado no Ubuntu com o Apache::

     sudo service apache2 reload


-------------------------------
Instalação para Desenvolvimento
-------------------------------

Para instalar ckanext-govdf_theme para desenvolvimento, ative o seu ambinete virtual do CKAN e digite::

    git clone https://lucas_jlma@bitbucket.org/lucas_jlma/gdf_ckan_theme.git
    cd ckanext-govdf_theme
    python setup.py develop
    pip install -r dev-requirements.txt

------------------
A ser implementado
------------------

Algumas funcionalidades não estão funcionando como deveriam e melhorias diversas devem ser implementadas.

* Ordenação de conteúdo em todas as páginas;
* Inclusão de CSS pelo fanstatic (ISSUE);
* Implementar ferramentas de acessibilidade;
* Implementar a área de administração do sistema;
* Traduzir strings personalizadas do sistema;
* links por referência;
* Estilizar a paginação;

Para que o template funcione perfeitamente é indicada a substituição do arquivo ``main.css`` por outro equivalente com as formatações específicas do template e assim a estrutura HTML também.


---------------------------------
Running the Tests - Not Available
---------------------------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.govdf_theme --cover-inclusive --cover-erase --cover-tests


---------------------------------------
Registering ckanext-govdf_theme on PyPI
---------------------------------------

ckanext-govdf_theme should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-govdf_theme. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------------
Releasing a New Version of ckanext-govdf_theme
----------------------------------------------

ckanext-govdf_theme is availabe on PyPI as https://pypi.python.org/pypi/ckanext-govdf_theme.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags