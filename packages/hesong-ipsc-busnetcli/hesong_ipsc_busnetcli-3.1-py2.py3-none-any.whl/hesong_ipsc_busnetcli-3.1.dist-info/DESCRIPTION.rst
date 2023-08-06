hesong-ipsc-busnetcli
#####################
IPSC专用的消息总线客户端的Python包装。

它用于向 Python_ 开发者提供SmartBus的客户端功能。

features
********

* 直接封装 `IPSC Data Bus` 的 `C` 语言客户端库 ipsc-bus-client_
* 采用 Python_ 标准库的 `ctypes` 进行 `C` 语言动态/共享库的封装。所以安装时不需要进行编译，理论上同时支持多种Python（如pypy,ironpython,jython）运行时（只要目标Python运行时支持ctypes）
* 完整的客户端功能包装,其功能基本上与 `C` 语言实现客户端一对一。

installation
************
(以 Ubuntu 1604 LTS 为例)

install ipsc-bus-client
=======================

下载依赖库 ipsc-bus-client_ ，将其 `include` 头文件复制到 `/usr/loca/include`, 库文件复制到 `/usr/local/lib`

.. code:: shell

    $ git clone https://bitbucket.org/hesong-opensource/ipsc-bus-client.git
    $ cd ipsc-bus-client
    $ sudo cp -af inc/*.h /usr/local/include
    $ sudo unzip -d /usr/local/lib lib/{{Platform}}-{{Architecture}}/libbusnetcli.zip
    $ sudo ldconfig

.. attention::

    有的操作系统可能并未将 `/usr/local/lib` 加入到库加载路径，请注意修改配置，确保路径正确。

install hesong-ipsc-busnetcli
=============================

online install with pip
-----------------------

pip_ 安装需要访问互联网

.. code:: shell

    pip install hesong-ipsc-busnetcli

offline install
---------------

.. code:: shell

    $ git clone https://bitbucket.org/hesong-opensource/ipsc-bus-client-python.git
    $ cd ipsc-bus-client-python
    $ sudo python setup.py install

.. _Python: http://www.python.org/
.. _pip: http://pip.pypa.io/
.. _ipsc-bus-client: http://bitbucket.org/hesong-opensource/ipsc-bus-client


