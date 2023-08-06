# Airbridge Utilities

## Installation
```
pip install airbridge
```

## Usage

### Testing
Set `.airbridgerc` on your project root folder or home directory before you run `from airbridge.testing import AirbridgeBaseTest`.


```
from airbridge.testing import AirbridgeBaseTest


class TestYourCode(AirbridgeBaseTest):

    def test_your_api(self):
        self.resource = "/api/v2/apps/your-app/your-resource"
        res = self.send_request(self.get_url())
        self.check_api_response(res)
```


### Worker
This 'QueueWorker' only works on [beanstlkd](http://kr.github.io/beanstalkd/).

```
from airbridge.worker import QueueWorker
import beanstalkc


BEANSTALKD_HOST = "your-beanstalkd-host"
BEANSTLAKD_PORT = 11300
QUEUE_NAME = "your-beanstalkd-queue-name"

def business_logic(what_to_do, **kwargs):

    if what_to_do == 'handle_your_method_1':
        # handle your method 1
        pass
    elif what_to_do == 'handle_your_method_2':
        # handle your method 2
        pass
    else:
        raise Exception('Not supported method.')


queue = beanstalkc.Connection(host=BEANSTALKD_HOST, port=BEANSTLAKD_PORT)
worker = QueueWorker(queue_engine=queue, queue_name=QUEUE_NAME)
worker.run(business_logic=business_logic)
```


### Utilities

```
from airbridge.utils.tools import is_empty

a = None
b = ""
print is_empty(a) # True
print is_empty(b) # True
```
