Welcome to the kount-access-python-sdk!
=====================================================


On these pages we'll discuss setting up and using the Kount Access product.

This library allows you to connect to the Kount Access API services and get information back from your login transactions. In order to use this library you will need:

#. A Merchant ID provided by Kount
#. An API Key generated for Kount Access
#. The Session ID used by the Data Collector
#. Login Information used by the user (login/password)


**Kount Access™** is designed for high-volume login, account creation and affiliate networks, cross-checking individual component with several other components to calculate the velocity of related login attempts, and providing the client with dozens of velocity checks and essential data to help determine the legitimacy of the user and account owners.

After the user submits their credentials for login (data collection completes), the merchant can request information about the device and then can request velocity details (the tallies of credential combinations
used) about the user's login attempt(s). Each response is returned in JSON format. With this information
the merchant can make business decisions on how it wants to react.

The **Kount Access API SDK** is used directly in the merchant's website (or authentication service) that
handles user login. The Kount Access API SDK should be integrated into the client code so that it is called
after the user submits their login, typically where the login form `POST` is handled. This will be used
regardless of whether the login is successful or not.


Downloading or Install the SDK
====================================================

If you want to use the Kount Access SDK, you need to download and build it locally. There are some options for downloading:

* **Clone** the ``kount-access-python-sdk`` repository and use its `master` branch if you want to have the latest (unreleased) features, improvements and bugfixes.

* **Download** (the latest) release from the `Releases <https://github.com/Kount/kount-access-python-sdk/releases>`_ page for a stable version of the SDK.

* **pip**

  ::

    pip install kount-access-sdk



.:information_source: This SDK is both Python 2.7.13 and 3.6.x compatible.




Setting up IDE projects
-------------------------------------------------

Komodo IDE/Edit, Scite, Visual Studio - have automatic python integration

Who do I talk to?
--------------------------

#. Repo owner or admin

#. Other community or team contact




