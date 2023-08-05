Agora.io Signal Python SDK
==========================

This is a wrapper of Agora signal APIs thats enables developers integrate Agora's signal service within 30 minutes.


Quick start example:

.. code-block:: python

    >>> from agorasigsdk.agora_signal import AgoraSgnal
    >>> from twisted.internet import reactor
    >>> appid = 'THIS_IS_YOUR_APPID.'
    >>> ag_sig = AgoraSignal(appid)
    >>> session = ag_sig.login('ACCOUNT_NAME', 'TOKEN', CALLBACK_CLASS_INSTANCE)
    >>> reactor.run()

Now you have a logged in Agora Signaling Session!


Installation
------------

.. code-block:: bash
    pip install agora-signaling-sdk

Easy and ready to go.


Documentation
-------------

Please find in https://docs.agora.io


