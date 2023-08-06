# Getting started

Mundipagg API

## How to Build


You must have Python 2 >=2.7.9 or Python 3 >=3.4 installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=MundiAPI-Python)


## How to Use

The following section explains how to use the Mundiapi SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=MundiAPI-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=MundiAPI-Python&projectName=mundiapi)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=MundiAPI-Python&projectName=mundiapi)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=MundiAPI-Python&projectName=mundiapi)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from mundiapi.mundiapi_client import MundiapiClient
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=MundiAPI-Python&libraryName=mundiapi.mundiapi_client&projectName=mundiapi)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=MundiAPI-Python&libraryName=mundiapi.mundiapi_client&projectName=mundiapi)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke 'pip install -r test-requirements.txt'
  3. Invoke 'nosetests'

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| basic_auth_user_name | The username to use with basic authentication |
| basic_auth_password | The password to use with basic authentication |



API client can be initialized as following.

```python
# Configuration parameters and credentials
basic_auth_user_name = 'basic_auth_user_name' # The username to use with basic authentication
basic_auth_password = 'basic_auth_password' # The password to use with basic authentication

client = MundiapiClient(basic_auth_user_name, basic_auth_password)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [ChargesController](#charges_controller)
* [CustomersController](#customers_controller)
* [SubscriptionsController](#subscriptions_controller)
* [PlansController](#plans_controller)
* [InvoicesController](#invoices_controller)
* [OrdersController](#orders_controller)
* [TokensController](#tokens_controller)

## <a name="charges_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ChargesController") ChargesController

### Get controller instance

An instance of the ``` ChargesController ``` class can be accessed from the API Client.

```python
 charges_client = client.charges
```

### <a name="get_charge"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.get_charge") get_charge

> Get a charge from its id

```python
def get_charge(self,
                   charge_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |



#### Example Usage

```python
charge_id = 'charge_id'

result = charges_client.get_charge(charge_id)

```


### <a name="retry_charge"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.retry_charge") retry_charge

> Retries a charge

```python
def retry_charge(self,
                     charge_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |



#### Example Usage

```python
charge_id = 'charge_id'

result = charges_client.retry_charge(charge_id)

```


### <a name="get_charges"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.get_charges") get_charges

> Lists all charges

```python
def get_charges(self)
```

#### Example Usage

```python

result = charges_client.get_charges()

```


### <a name="create_charge"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.create_charge") create_charge

> Creates a new charge

```python
def create_charge(self,
                      request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| request |  ``` Required ```  | Request for creating a charge |



#### Example Usage

```python
request = CreateChargeRequest()

result = charges_client.create_charge(request)

```


### <a name="update_charge_card"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.update_charge_card") update_charge_card

> Updates the card from a charge

```python
def update_charge_card(self,
                           charge_id,
                           request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |
| request |  ``` Required ```  | Request for updating a charge's card |



#### Example Usage

```python
charge_id = 'charge_id'
request = UpdateChargeCardRequest()

result = charges_client.update_charge_card(charge_id, request)

```


### <a name="update_charge_payment_method"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.update_charge_payment_method") update_charge_payment_method

> Updates a charge's payment method

```python
def update_charge_payment_method(self,
                                     charge_id,
                                     request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |
| request |  ``` Required ```  | Request for updating the payment method from a charge |



#### Example Usage

```python
charge_id = 'charge_id'
request = UpdateChargePaymentMethodRequest()

result = charges_client.update_charge_payment_method(charge_id, request)

```


### <a name="cancel_charge"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.cancel_charge") cancel_charge

> Cancel a charge

```python
def cancel_charge(self,
                      charge_id,
                      request=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |
| request |  ``` Optional ```  | Request for cancelling a charge |



#### Example Usage

```python
charge_id = 'charge_id'
request = CreateCancelChargeRequest()

result = charges_client.cancel_charge(charge_id, request)

```


### <a name="capture_charge"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.capture_charge") capture_charge

> Captures a charge

```python
def capture_charge(self,
                       charge_id,
                       request=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | Charge id |
| request |  ``` Optional ```  | Request for capturing a charge |



#### Example Usage

```python
charge_id = 'charge_id'
request = CreateCaptureChargeRequest()

result = charges_client.capture_charge(charge_id, request)

```


### <a name="update_charge_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".ChargesController.update_charge_metadata") update_charge_metadata

> Updates the metadata from a charge

```python
def update_charge_metadata(self,
                               charge_id,
                               request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| chargeId |  ``` Required ```  | The charge id |
| request |  ``` Required ```  | Request for updating the charge metadata |



#### Example Usage

```python
charge_id = 'charge_id'
request = UpdateMetadataRequest()

result = charges_client.update_charge_metadata(charge_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="customers_controller"></a>![Class: ](https://apidocs.io/img/class.png ".CustomersController") CustomersController

### Get controller instance

An instance of the ``` CustomersController ``` class can be accessed from the API Client.

```python
 customers_client = client.customers
```

### <a name="get_addresses"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_addresses") get_addresses

> Gets all adressess from a customer

```python
def get_addresses(self,
                      customer_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer id |



#### Example Usage

```python
customer_id = 'customer_id'

result = customers_client.get_addresses(customer_id)

```


### <a name="get_cards"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_cards") get_cards

> Get all cards from a customer

```python
def get_cards(self,
                  customer_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |



#### Example Usage

```python
customer_id = 'customer_id'

result = customers_client.get_cards(customer_id)

```


### <a name="create_customer"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.create_customer") create_customer

> Creates a new customer

```python
def create_customer(self,
                        request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| request |  ``` Required ```  | Request for creating a customer |



#### Example Usage

```python
request = CreateCustomerRequest()

result = customers_client.create_customer(request)

```


### <a name="get_customer"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_customer") get_customer

> Get a customer

```python
def get_customer(self,
                     customer_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |



#### Example Usage

```python
customer_id = 'customer_id'

result = customers_client.get_customer(customer_id)

```


### <a name="update_address"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.update_address") update_address

> Updates an address

```python
def update_address(self,
                       customer_id,
                       address_id,
                       request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| addressId |  ``` Required ```  | Address Id |
| request |  ``` Required ```  | Request for updating an address |



#### Example Usage

```python
customer_id = 'customer_id'
address_id = 'address_id'
request = UpdateAddressRequest()

result = customers_client.update_address(customer_id, address_id, request)

```


### <a name="update_card"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.update_card") update_card

> Updates a card

```python
def update_card(self,
                    customer_id,
                    card_id,
                    request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| cardId |  ``` Required ```  | Card id |
| request |  ``` Required ```  | Request for updating a card |



#### Example Usage

```python
customer_id = 'customer_id'
card_id = 'card_id'
request = UpdateCardRequest()

result = customers_client.update_card(customer_id, card_id, request)

```


### <a name="get_address"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_address") get_address

> Get a customer's address

```python
def get_address(self,
                    customer_id,
                    address_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer id |
| addressId |  ``` Required ```  | Address Id |



#### Example Usage

```python
customer_id = 'customer_id'
address_id = 'address_id'

result = customers_client.get_address(customer_id, address_id)

```


### <a name="delete_address"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.delete_address") delete_address

> Delete a Customer's address

```python
def delete_address(self,
                       customer_id,
                       address_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| addressId |  ``` Required ```  | Address Id |



#### Example Usage

```python
customer_id = 'customer_id'
address_id = 'address_id'

result = customers_client.delete_address(customer_id, address_id)

```


### <a name="delete_card"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.delete_card") delete_card

> Delete a customer's card

```python
def delete_card(self,
                    customer_id,
                    card_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| cardId |  ``` Required ```  | Card Id |



#### Example Usage

```python
customer_id = 'customer_id'
card_id = 'card_id'

result = customers_client.delete_card(customer_id, card_id)

```


### <a name="create_address"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.create_address") create_address

> Creates a new address for a customer

```python
def create_address(self,
                       customer_id,
                       request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| request |  ``` Required ```  | Request for creating an address |



#### Example Usage

```python
customer_id = 'customer_id'
request = CreateAddressRequest()

result = customers_client.create_address(customer_id, request)

```


### <a name="get_card"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_card") get_card

> Get a customer's card

```python
def get_card(self,
                 customer_id,
                 card_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer id |
| cardId |  ``` Required ```  | Card id |



#### Example Usage

```python
customer_id = 'customer_id'
card_id = 'card_id'

result = customers_client.get_card(customer_id, card_id)

```


### <a name="create_card"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.create_card") create_card

> Creates a new card for a customer

```python
def create_card(self,
                    customer_id,
                    request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer id |
| request |  ``` Required ```  | Request for creating a card |



#### Example Usage

```python
customer_id = 'customer_id'
request = CreateCardRequest()

result = customers_client.create_card(customer_id, request)

```


### <a name="update_customer"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.update_customer") update_customer

> Updates a customer

```python
def update_customer(self,
                        customer_id,
                        request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer id |
| request |  ``` Required ```  | Request for updating a customer |



#### Example Usage

```python
customer_id = 'customer_id'
request = UpdateCustomerRequest()

result = customers_client.update_customer(customer_id, request)

```


### <a name="delete_access_tokens"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.delete_access_tokens") delete_access_tokens

> Delete a Customer's access tokens

```python
def delete_access_tokens(self,
                             customer_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |



#### Example Usage

```python
customer_id = 'customer_id'

result = customers_client.delete_access_tokens(customer_id)

```


### <a name="get_access_tokens"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_access_tokens") get_access_tokens

> Get all access tokens from a customer

```python
def get_access_tokens(self,
                          customer_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |



#### Example Usage

```python
customer_id = 'customer_id'

result = customers_client.get_access_tokens(customer_id)

```


### <a name="get_customers"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_customers") get_customers

> Get all Customers

```python
def get_customers(self,
                      name=None,
                      document=None,
                      page=1,
                      size=10)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| name |  ``` Optional ```  | Name of the Customer |
| document |  ``` Optional ```  | Document of the Customer |
| page |  ``` Optional ```  ``` DefaultValue ```  | Current page the the search |
| size |  ``` Optional ```  ``` DefaultValue ```  | Quantity pages of the search |



#### Example Usage

```python
name = 'name'
document = 'document'
page = 1
size = 10

result = customers_client.get_customers(name, document, page, size)

```


### <a name="delete_access_token"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.delete_access_token") delete_access_token

> Delete a customer's access token

```python
def delete_access_token(self,
                            customer_id,
                            token_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| tokenId |  ``` Required ```  | Token Id |



#### Example Usage

```python
customer_id = 'customer_id'
token_id = 'token_id'

result = customers_client.delete_access_token(customer_id, token_id)

```


### <a name="create_access_token"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.create_access_token") create_access_token

> Creates a access token for a customer

```python
def create_access_token(self,
                            customer_id,
                            request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| request |  ``` Required ```  | Request for creating a access token |



#### Example Usage

```python
customer_id = 'customer_id'
request = CreateAccessTokenRequest()

result = customers_client.create_access_token(customer_id, request)

```


### <a name="get_access_token"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.get_access_token") get_access_token

> Get a Customer's access token

```python
def get_access_token(self,
                         customer_id,
                         token_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | Customer Id |
| tokenId |  ``` Required ```  | Token Id |



#### Example Usage

```python
customer_id = 'customer_id'
token_id = 'token_id'

result = customers_client.get_access_token(customer_id, token_id)

```


### <a name="update_customer_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".CustomersController.update_customer_metadata") update_customer_metadata

> Updates the metadata a customer

```python
def update_customer_metadata(self,
                                 customer_id,
                                 request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| customerId |  ``` Required ```  | The customer id |
| request |  ``` Required ```  | Request for updating the customer metadata |



#### Example Usage

```python
customer_id = 'customer_id'
request = UpdateMetadataRequest()

result = customers_client.update_customer_metadata(customer_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="subscriptions_controller"></a>![Class: ](https://apidocs.io/img/class.png ".SubscriptionsController") SubscriptionsController

### Get controller instance

An instance of the ``` SubscriptionsController ``` class can be accessed from the API Client.

```python
 subscriptions_client = client.subscriptions
```

### <a name="update_subscription_billing_date"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.update_subscription_billing_date") update_subscription_billing_date

> Updates the billing date from a subscription

```python
def update_subscription_billing_date(self,
                                         subscription_id,
                                         request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | The subscription id |
| request |  ``` Required ```  | Request for updating the subscription billing date |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = UpdateSubscriptionBillingDateRequest()

result = subscriptions_client.update_subscription_billing_date(subscription_id, request)

```


### <a name="create_usage"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.create_usage") create_usage

> Creates a usage

```python
def create_usage(self,
                     subscription_id,
                     item_id,
                     body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription Id |
| itemId |  ``` Required ```  | Item id |
| body |  ``` Required ```  | Request for creating a usage |



#### Example Usage

```python
subscription_id = 'subscription_id'
item_id = 'item_id'
body = CreateUsageRequest()

result = subscriptions_client.create_usage(subscription_id, item_id, body)

```


### <a name="update_subscription_item"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.update_subscription_item") update_subscription_item

> Updates a subscription item

```python
def update_subscription_item(self,
                                 subscription_id,
                                 item_id,
                                 body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription Id |
| itemId |  ``` Required ```  | Item id |
| body |  ``` Required ```  | Request for updating a subscription item |



#### Example Usage

```python
subscription_id = 'subscription_id'
item_id = 'item_id'
body = UpdateSubscriptionItemRequest()

result = subscriptions_client.update_subscription_item(subscription_id, item_id, body)

```


### <a name="get_subscriptions"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.get_subscriptions") get_subscriptions

> Gets all subscriptions

```python
def get_subscriptions(self)
```

#### Example Usage

```python

result = subscriptions_client.get_subscriptions()

```


### <a name="update_subscription_card"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.update_subscription_card") update_subscription_card

> Updates the credit card from a subscription

```python
def update_subscription_card(self,
                                 subscription_id,
                                 request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| request |  ``` Required ```  | Request for updating a card |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = UpdateSubscriptionCardRequest()

result = subscriptions_client.update_subscription_card(subscription_id, request)

```


### <a name="create_subscription"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.create_subscription") create_subscription

> Creates a new subscription

```python
def create_subscription(self,
                            body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Request for creating a subscription |



#### Example Usage

```python
body = CreateSubscriptionRequest()

result = subscriptions_client.create_subscription(body)

```


### <a name="create_subscription_item"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.create_subscription_item") create_subscription_item

> Creates a new Subscription item

```python
def create_subscription_item(self,
                                 subscription_id,
                                 request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| request |  ``` Required ```  | Request for creating a subscription item |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = CreateSubscriptionItemRequest()

result = subscriptions_client.create_subscription_item(subscription_id, request)

```


### <a name="create_discount"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.create_discount") create_discount

> Creates a discount

```python
def create_discount(self,
                        subscription_id,
                        request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| request |  ``` Required ```  | Request for creating a discount |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = CreateDiscountRequest()

result = subscriptions_client.create_discount(subscription_id, request)

```


### <a name="get_subscription"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.get_subscription") get_subscription

> Gets a subscription

```python
def get_subscription(self,
                         subscription_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |



#### Example Usage

```python
subscription_id = 'subscription_id'

result = subscriptions_client.get_subscription(subscription_id)

```


### <a name="update_subscription_payment_method"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.update_subscription_payment_method") update_subscription_payment_method

> Updates the payment method from a subscription

```python
def update_subscription_payment_method(self,
                                           subscription_id,
                                           request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| request |  ``` Required ```  | Request for updating the paymentmethod from a subscription |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = UpdateSubscriptionPaymentMethodRequest()

result = subscriptions_client.update_subscription_payment_method(subscription_id, request)

```


### <a name="get_usages"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.get_usages") get_usages

> Lists all usages from a subscription item

```python
def get_usages(self,
                   subscription_id,
                   item_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | The subscription id |
| itemId |  ``` Required ```  | The subscription item id |



#### Example Usage

```python
subscription_id = 'subscription_id'
item_id = 'item_id'

result = subscriptions_client.get_usages(subscription_id, item_id)

```


### <a name="delete_usage"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.delete_usage") delete_usage

> Deletes a usage

```python
def delete_usage(self,
                     subscription_id,
                     item_id,
                     usage_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | The subscription id |
| itemId |  ``` Required ```  | The subscription item id |
| usageId |  ``` Required ```  | The usage id |



#### Example Usage

```python
subscription_id = 'subscription_id'
item_id = 'item_id'
usage_id = 'usage_id'

result = subscriptions_client.delete_usage(subscription_id, item_id, usage_id)

```


### <a name="delete_discount"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.delete_discount") delete_discount

> Deletes a discount

```python
def delete_discount(self,
                        subscription_id,
                        discount_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| discountId |  ``` Required ```  | Discount Id |



#### Example Usage

```python
subscription_id = 'subscription_id'
discount_id = 'discount_id'

result = subscriptions_client.delete_discount(subscription_id, discount_id)

```


### <a name="cancel_subscription"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.cancel_subscription") cancel_subscription

> Cancels a subscription

```python
def cancel_subscription(self,
                            subscription_id,
                            request=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| request |  ``` Optional ```  | Request for cancelling a subscription |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = CreateCancelSubscriptionRequest()

result = subscriptions_client.cancel_subscription(subscription_id, request)

```


### <a name="delete_subscription_item"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.delete_subscription_item") delete_subscription_item

> Deletes a subscription item

```python
def delete_subscription_item(self,
                                 subscription_id,
                                 subscription_item_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | Subscription id |
| subscriptionItemId |  ``` Required ```  | Subscription item id |



#### Example Usage

```python
subscription_id = 'subscription_id'
subscription_item_id = 'subscription_item_id'

result = subscriptions_client.delete_subscription_item(subscription_id, subscription_item_id)

```


### <a name="update_subscription_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".SubscriptionsController.update_subscription_metadata") update_subscription_metadata

> Updates the metadata from a subscription

```python
def update_subscription_metadata(self,
                                     subscription_id,
                                     request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subscriptionId |  ``` Required ```  | The subscription id |
| request |  ``` Required ```  | Request for updating the subscrption metadata |



#### Example Usage

```python
subscription_id = 'subscription_id'
request = UpdateMetadataRequest()

result = subscriptions_client.update_subscription_metadata(subscription_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="plans_controller"></a>![Class: ](https://apidocs.io/img/class.png ".PlansController") PlansController

### Get controller instance

An instance of the ``` PlansController ``` class can be accessed from the API Client.

```python
 plans_client = client.plans
```

### <a name="update_plan_item"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.update_plan_item") update_plan_item

> Updates a plan item

```python
def update_plan_item(self,
                         plan_id,
                         plan_item_id,
                         body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |
| planItemId |  ``` Required ```  | Plan item id |
| body |  ``` Required ```  | Request for updating the plan item |



#### Example Usage

```python
plan_id = 'plan_id'
plan_item_id = 'plan_item_id'
body = UpdatePlanItemRequest()

result = plans_client.update_plan_item(plan_id, plan_item_id, body)

```


### <a name="get_plan"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.get_plan") get_plan

> Gets a plan

```python
def get_plan(self,
                 plan_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |



#### Example Usage

```python
plan_id = 'plan_id'

result = plans_client.get_plan(plan_id)

```


### <a name="create_plan_item"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.create_plan_item") create_plan_item

> Adds a new item to a plan

```python
def create_plan_item(self,
                         plan_id,
                         request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |
| request |  ``` Required ```  | Request for creating a plan item |



#### Example Usage

```python
plan_id = 'plan_id'
request = CreatePlanItemRequest()

result = plans_client.create_plan_item(plan_id, request)

```


### <a name="update_plan"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.update_plan") update_plan

> Updates a plan

```python
def update_plan(self,
                    plan_id,
                    request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |
| request |  ``` Required ```  | Request for updating a plan |



#### Example Usage

```python
plan_id = 'plan_id'
request = UpdatePlanRequest()

result = plans_client.update_plan(plan_id, request)

```


### <a name="create_plan"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.create_plan") create_plan

> Creates a new plan

```python
def create_plan(self,
                    body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Request for creating a plan |



#### Example Usage

```python
body = CreatePlanRequest()

result = plans_client.create_plan(body)

```


### <a name="get_plans"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.get_plans") get_plans

> Gets all plans

```python
def get_plans(self)
```

#### Example Usage

```python

result = plans_client.get_plans()

```


### <a name="delete_plan"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.delete_plan") delete_plan

> Deletes a plan

```python
def delete_plan(self,
                    plan_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |



#### Example Usage

```python
plan_id = 'plan_id'

result = plans_client.delete_plan(plan_id)

```


### <a name="get_plan_item"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.get_plan_item") get_plan_item

> Gets a plan item

```python
def get_plan_item(self,
                      plan_id,
                      plan_item_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |
| planItemId |  ``` Required ```  | Plan item id |



#### Example Usage

```python
plan_id = 'plan_id'
plan_item_id = 'plan_item_id'

result = plans_client.get_plan_item(plan_id, plan_item_id)

```


### <a name="delete_plan_item"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.delete_plan_item") delete_plan_item

> Removes an item from a plan

```python
def delete_plan_item(self,
                         plan_id,
                         plan_item_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | Plan id |
| planItemId |  ``` Required ```  | Plan item id |



#### Example Usage

```python
plan_id = 'plan_id'
plan_item_id = 'plan_item_id'

result = plans_client.delete_plan_item(plan_id, plan_item_id)

```


### <a name="update_plan_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".PlansController.update_plan_metadata") update_plan_metadata

> Updates the metadata from a plan

```python
def update_plan_metadata(self,
                             plan_id,
                             request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| planId |  ``` Required ```  | The plan id |
| request |  ``` Required ```  | Request for updating the plan metadata |



#### Example Usage

```python
plan_id = 'plan_id'
request = UpdateMetadataRequest()

result = plans_client.update_plan_metadata(plan_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="invoices_controller"></a>![Class: ](https://apidocs.io/img/class.png ".InvoicesController") InvoicesController

### Get controller instance

An instance of the ``` InvoicesController ``` class can be accessed from the API Client.

```python
 invoices_client = client.invoices
```

### <a name="cancel_invoice"></a>![Method: ](https://apidocs.io/img/method.png ".InvoicesController.cancel_invoice") cancel_invoice

> Cancels an invoice

```python
def cancel_invoice(self,
                       invoice_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| invoiceId |  ``` Required ```  | Invoice id |



#### Example Usage

```python
invoice_id = 'invoice_id'

result = invoices_client.cancel_invoice(invoice_id)

```


### <a name="get_last_invoice_charge"></a>![Method: ](https://apidocs.io/img/method.png ".InvoicesController.get_last_invoice_charge") get_last_invoice_charge

> Gets the last charge from an invoice

```python
def get_last_invoice_charge(self,
                                invoice_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| invoiceId |  ``` Required ```  | Invoice id |



#### Example Usage

```python
invoice_id = 'invoice_id'

result = invoices_client.get_last_invoice_charge(invoice_id)

```


### <a name="get_invoices"></a>![Method: ](https://apidocs.io/img/method.png ".InvoicesController.get_invoices") get_invoices

> Gets all invoices

```python
def get_invoices(self)
```

#### Example Usage

```python

result = invoices_client.get_invoices()

```


### <a name="get_invoice"></a>![Method: ](https://apidocs.io/img/method.png ".InvoicesController.get_invoice") get_invoice

> Gets an invoice

```python
def get_invoice(self,
                    invoice_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| invoiceId |  ``` Required ```  | Invoice Id |



#### Example Usage

```python
invoice_id = 'invoice_id'

result = invoices_client.get_invoice(invoice_id)

```


### <a name="update_invoice_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".InvoicesController.update_invoice_metadata") update_invoice_metadata

> Updates the metadata from an invoice

```python
def update_invoice_metadata(self,
                                invoice_id,
                                request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| invoiceId |  ``` Required ```  | The invoice id |
| request |  ``` Required ```  | Request for updating the invoice metadata |



#### Example Usage

```python
invoice_id = 'invoice_id'
request = UpdateMetadataRequest()

result = invoices_client.update_invoice_metadata(invoice_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="orders_controller"></a>![Class: ](https://apidocs.io/img/class.png ".OrdersController") OrdersController

### Get controller instance

An instance of the ``` OrdersController ``` class can be accessed from the API Client.

```python
 orders_client = client.orders
```

### <a name="get_order"></a>![Method: ](https://apidocs.io/img/method.png ".OrdersController.get_order") get_order

> Gets an order

```python
def get_order(self,
                  order_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| orderId |  ``` Required ```  | Order id |



#### Example Usage

```python
order_id = 'order_id'

result = orders_client.get_order(order_id)

```


### <a name="get_orders"></a>![Method: ](https://apidocs.io/img/method.png ".OrdersController.get_orders") get_orders

> Gets all orders

```python
def get_orders(self)
```

#### Example Usage

```python

result = orders_client.get_orders()

```


### <a name="create_order"></a>![Method: ](https://apidocs.io/img/method.png ".OrdersController.create_order") create_order

> Creates a new Order

```python
def create_order(self,
                     body)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| body |  ``` Required ```  | Request for creating an order |



#### Example Usage

```python
body = CreateOrderRequest()

result = orders_client.create_order(body)

```


### <a name="update_order_metadata"></a>![Method: ](https://apidocs.io/img/method.png ".OrdersController.update_order_metadata") update_order_metadata

> Updates the metadata from an order

```python
def update_order_metadata(self,
                              order_id,
                              request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| orderId |  ``` Required ```  | The order id |
| request |  ``` Required ```  | Request for updating the order metadata |



#### Example Usage

```python
order_id = 'order_id'
request = UpdateMetadataRequest()

result = orders_client.update_order_metadata(order_id, request)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="tokens_controller"></a>![Class: ](https://apidocs.io/img/class.png ".TokensController") TokensController

### Get controller instance

An instance of the ``` TokensController ``` class can be accessed from the API Client.

```python
 tokens_client = client.tokens
```

### <a name="get_token"></a>![Method: ](https://apidocs.io/img/method.png ".TokensController.get_token") get_token

> *Tags:*  ``` Skips Authentication ``` 

> Gets a token from its id

```python
def get_token(self,
                  id,
                  public_key)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| id |  ``` Required ```  | Token id |
| publicKey |  ``` Required ```  | Public key |



#### Example Usage

```python
id = 'id'
public_key = 'public_key'

result = tokens_client.get_token(id, public_key)

```


### <a name="create_token"></a>![Method: ](https://apidocs.io/img/method.png ".TokensController.create_token") create_token

> *Tags:*  ``` Skips Authentication ``` 

> TODO: Add a method description

```python
def create_token(self,
                     public_key,
                     request)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| publicKey |  ``` Required ```  | Public key |
| request |  ``` Required ```  | Request for creating a token |



#### Example Usage

```python
public_key = 'public_key'
request = CreateTokenRequest()

result = tokens_client.create_token(public_key, request)

```


[Back to List of Controllers](#list_of_controllers)



