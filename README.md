# Custom component for Airthings for business

## Setup
First of all, you need a business account (wont work on consumer accounts for the moment) to make this work.
Log into the dashboard, and go to [Create a new API integration](https://dashboard.airthings.com/integrations/api-integration/add-api-client) (Integrations -> API -> Create new).

### Create integration on Airthings for Business dashboard
- Give the integration a name
- *Scope*: Read device
- *Access type*: Confidential
- *Flow-type*: Authorization code
- Set *Redirect URI* to http://localhost:8123/auth/external/callback (change http://localhost:8123 to your own address)

### Add configuration entry into Home Assistant
When you've created a integration in the dashboard, then go and find the client ID on top next to the name, and click *Display secret* to get the value for `client_secret`. 

If you have access to multiple organizations, but you only want to show one of them in Home Assistant, you can also add the organization ID to the configuration.

#### Example configuration.yaml
Add `airthings_client_id` and `airthings_client_secret` for the Airthings API into your `secrets.yaml` file.

Add this to your configuration file:
```
airthings:
  client_id: !secret airthings_client_id
  client_secret: !secret airthings_client_secret
  organization_id: !secret airthings_organization_id (OPTIONAL)
```

## Example
There is an example configuration in the [homeassistant](./homeassistant)-folder. You need to add a `secrets.yaml` file that contains the client id and secret. 

### Running example configuration with Docker compose
```
docker-compose up --remove-orphans --build homeassistant
```

* Open http://localhost:8123/
* Create an account
* Go to Configuration -> Integrations
* Add integration for Airthings

#### Bonus stuff
* Add integration for HACS
* Upgrade the HACS dependencies
* Go to the overview tab to see your entities and sensor values
