==========
pywe-oauth
==========

Wechat Oauth Module for Python.

Installation
============

::

    pip install pywe-oauth


Usage
=====

::

    from pywe_oauth import get_access_info, get_oauth_code_url, get_userinfo, get_oauth_redirect_url


Method
======

::

    def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None):

    def get_access_info(self, appid=None, secret=None, code=None):

    def get_userinfo(self, access_token=None, openid=None):

    def get_oauth_redirect_url(self, oauth_uri, scope='snsapi_base', redirect_url=None, default_url=None):

