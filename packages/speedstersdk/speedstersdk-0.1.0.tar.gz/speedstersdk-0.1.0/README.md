# Speedster SDK

## Installing the SDK

Add `git+ssh://git@pdihub.hi.inet/smartdigits/speedster-sdk.git` to the speedster's requirements.txt file.

This repository depends on the SmartDigits Utils ([smd-utils](https://pdihub.hi.inet/smartdigits/smd-utils)) repo which means that the SDK needs to be installed as follows:

```bash
pip install -r requirements.txt \
-i https://artifactory.hi.inet/artifactory/api/pypi/pypi/simple \
--trusted-host artifactory.hi.inet
```

## Creating Speedster
A new speedster should use the speedster sdk, by creating a class which inherits from the 
InsightResolver class in the speedster sdk.

```python

# Import the Insight Resolver class
from speedstersdk.insight.resolver import InsightResolver

# the speedster should inherit the Insight Resover class from the sdk library
class ExampleInsightResolver(InsightResolver):

# It should implement the resolve method, where it processes each event procedding from the
# backlogger. They way of resolving the event will depend on the data source.

    def resolve(self, event):
        data = event['payload']
        msisdn = data["MSISDN"]

        insight_name = "OK"
        
        # it is required to update the different insight associated to the msisdn by
        # using the update_insight method of the parent class
        self.update_insight(msisdn, insight_name, event)
        # finally it stores the data in dormer
        self.save_updated_insights()
```

# Running tests

To run the included tests you can use the makefile.

```bash
make clean build
make test
make clean
```
