# Cumulocity MQTT Python Agent

Template: [https://www.cumulocity.com/guides/mqtt/hello-mqtt-python/](https://www.cumulocity.com/guides/mqtt/hello-mqtt-python/)

**Environment Variables:**
    
	C8Y_USER
	C8Y_PASS
	C8Y_TENANT
	C8Y_BASE_URL
	C8Y_SERVER_HOST
	C8Y_CLIENT_ID
	C8Y_CLIENT_MODEL

**Example (in ~/.bashrc or ~/.bash_profile):**

	export C8Y_USER=apiuser
	export C8Y_PASS=oka*****
	export C8Y_TENANT=infrastructure
	export C8Y_BASE_URL=sbdconnect.io
	export C8Y_SERVER_HOST=infrastructure.sbdconnect.io
	export C8Y_CLIENT_ID=14.195066.1333
	export C8Y_CLIENT_MODEL=ESX-TC3G

**Use:**

* Connects device to Cumulocity
* Updates device location using an external REST call
* Sends random measurement values

**Installation:**

	git clone git@bitbucket.org:iotarchitecture/cumulocity-client-python.git
	cd cumulocity-client-python
	python setup.py install

**Running as a process:**

	cumulocity_client > /dev/null 2>&1 &