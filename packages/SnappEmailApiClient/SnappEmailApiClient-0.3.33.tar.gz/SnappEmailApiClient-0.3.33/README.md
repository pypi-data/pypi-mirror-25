# ApiClient.py


## Build
#### Generate new classes
- Update data contract file: `generate/SdkWebServiceDataContract.xsd`
- Run `generate/iterable_names.py`:
- Run GenerateDS (`pip install generateds`) `C:\Users\uroshe\AppData\Local\Programs\Python\Python35-32\Scripts\generateDS.py -a "bc:" -o "snapp_email\datacontract\classes.py" -s "snapp_email\datacontract\subclasses.py" --export="" --member-specs="dict" snapp_email\generate\SdkWebServiceDataContract.xsd`

#### Generate new endpoints
- Update API Index file: `generate/api-index.json`
- Run `generate/generate.py`

#### Run tests

#### Push to git and publish the new version on GitHub
- Change `PACKAGE_VERSION` in `api_client.py`
- Commit (& push)
- git tag -a v0.3.19 HEAD -m "v0.3.19 released" && git push origin v0.3.19

#### Upload new version to Python Package Index
- python setup.py sdist upload -r pypi


## Examples
Examples on posting messages can be found in: `samples/example-post.py`. More examples in `messaging.py` and `tests/`.
Making API calls in general: `api_client.<endpoint>.<resource>.(create|get|update|delete|options)`.
Endpoint for a resource can be found in API Index file.

#### Creating a new resource
To create a new resource `ExampleResource`:
```
from snapp_email import ApiClient
from snapp_email.datacontract.classes import ExampleResource

api_client = ApiClient(...)  # Instantiate api client with credentials

# Instantiate new object instance that you want to create with some attributes.
my_object = ExampleResource(attribute1=value1, attribute2=value2, ...)

# Make a CREATE API call for the ExampleResource resource
created_object = api_client.example.ExampleResource.create(my_object)
```

#### Getting a resource
```
api_client.example.ExampleResource.get(resource_id)
```


## FAQ
##### How to use a certificate?
`api_client = ApiClient(..., certificate="/path/to/certificate")`
##### How to change the environment?
`api_client = ApiClient(..., api_url="https://new-api.url")`