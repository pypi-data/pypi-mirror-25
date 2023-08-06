# WebInspect API Documentation

The webinspect-api module contains a class that wraps the WebInspect RESTful calls in a response object.  The class WebInspectApi class contains a set of prepared `GET` and `POST` calls.


## Table of Contents
[Constructor](#constructor)

[Response Object](#response-object)

[Scanner](#scanner)

- [Continue scan: `continue_scan`](#continue-scan)
- [Create scan: `create_scan`](#create-scan)
- [Delete scan: `delete_scan`](#delete-scan)
- [Export scan format: `export_scan_format`](#export-scan-format)
- [Get current status: `get_current_status`](#get-current-status)
- [Get scan by name: `get_scan_by_name`](#get-scan-by-name)
- [Get scan issues: `get_scan_issues`](#get-scan-issues)
- [Get scan log: `get_scan_log`](#get-scan-log)
- [List scans: `list_scans`](#list-scans)
- [List settings: `list_settings`](#list-settings)
- [List webmacros: `list_webmacros`](#list-webmacros)
- [Stop scan: `stop_scan`](#stop-scan)
- [Upload settings: `upload_settings`](#upload-settings)
- [Upload webmacro: `upload_webmacro`](#upload-webmacro)

[SecureBase](#securebase)

- [Delete policy: `delete_policy`](#delete-policy)
- [Get policy by guid: `get_policy_by_guid`](#get-policy-by-guid)
- [Get policy by name: `get_policy_by_name`](#get-policy-by-name)
- [List policies: `list_policies`](#list-policies)
- [Upload policy: `upload_policy`](#upload-policy)


## Constructor
The constructor requires only one value - the host address of the WebInspect API. All others are optional.

#### Required parameters
*host* - The address of the WebInspect API

#### Optional parameters
*username* - If the API is configured for basic auth, both username and password must be provided.<br>
*password* - If the API is configured for basic auth, both username and password must be provided.<br>
*verify_ssl* - Defaults to true. To disable verification of an HTTPS connection to the API, set to False.<br>
*user_agent* - User agent for requests.<br>
*cert* - If the API is configured for client-certificate based auth, the path to the client certificate.
- - -

## Response object

All calls in this module return an object having the following properties and methods.

### Properties
*success* - a boolean indicating if the call was successful or not. True indicates a successful call, while False indicates an unsuccessful call.<br>
*response_code* - the actual HTTP response code from the call to the WebInspect server.<br>
*message* - if the call was successful, message is 'OK'. If the call was not successful, message is descriptive text of the failure. e.g. An SSL error occurred, etc.<br>
*data* - the data (if any) returned from the WebInspect API.<br>

### Methods
*data_json()* - Returns object data as JSON. An optional boolean parameter (pretty), if set to True, will return pretty-formatted JSON.

Below is an example of constructing a WebInspectAPI class, calling a method, and exploring the response.

```python

>>> from webinspectapi import webinspect

>>> wi = webinspect.WebInspectApi('http://myserver.com:8083')

>>> response = wi.list_scans()

>>> response.success
True

>>> response.response_code
200

>>> response.message
'OK'

>>> print response.data_json(pretty=True)
[
    {
        "ID": "01234567-89ab-cdef-0123-456789abcdef",
        "Name": "a_scan_that_ran",
        "StartTime": "2016-12-09T13:48:25.993",
        "Status": "Complete"
    },
    ...
```
- - -

## Scanner

### Continue Scan: `continue_scan`
Resume a stopped scan.

#### Parameters
*scan_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.continue_scan('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Create Scan: `create_scan`

A new scan can be created by specifying a settings file that exists in the WebInspect scan settings folder.
Overrides are optional and provide a way to make changes to certain fields in the referenced scan settings file.

#### Parameters

*settings*<br>
*scan_name*

#### Example

```python
wi = webinspect.WebInspectAPI(host)
response = wi.create_scan(riches, riches-20160905)
```
- - -

### Delete scan: `delete_scan`
Delete an existing scan.

#### Parameters
*scan_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.delete_scan('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Export scan format: `export_scan_format`
Export and download an existing scan in the specified format. Details of supported format and detail type are in the formal HP WebInspect documentation.

#### Parameters
*scan_id*<br>
*extension*<br>
*detail_type* (optional)

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.export_scan_format('01234567-89ab-cdef-0123-456789abcdef','issue')
```
- - -

### Get current status: `get_current_status`
Retrieve the status of an existing scan

#### Parameters
*scan_id*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_current_status('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Get scan by name: `get_scan_by_name`
Retrieve an existing scan

#### Parameters
*scan_name*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_scan_by_name('some_scan')
```
- - -

### Get scan issues: `get_scan_issues`
Retrieve issues identified by a scan.

#### Parameters
*scan_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_scan_issues('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Get scan log: `get_scan_log`
Retrieve the log generated by a scan

#### Parameters
*scan_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_scan_log('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### List scans: `list_scans`
Retrieve a list of existing scans

#### Parameters
*none*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.list_scans()
```
- - -

### List settings: `list_settings`
Retrieve a list of existing settings

#### Parameters
*none*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.list_settings()
```
- - -

### List webmacros: `list_webmacros`
Retrieve a list of webmacros

#### Parameters
*none*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.list_webmacros()
```
- - -

### Stop scan: `stop_scan`
Stop an existing scan

#### Parameters
*scan_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.stop_scan('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Upload settings: `upload_settings`
Upload a settings file to the server

#### Parameters
*settings_file_path*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.upload_settings('/User/workspace/some_settings.xml')
```
- - -

### Upload webmacro: `upload_webmacro`
Upload a webmacro file to the server

#### Parameters
*macro_file_path*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.upload_webmacro('/User/workspace/some_macro.webmacro')
```
- - -

### Wait for status change: `wait_for_status_change`
Wait for the identified scan's status to change. This call will not return until the scan status changes, or until the server connection is lost.

#### Parameters
*scan_id*


#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.wait_for_status_change('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

## SecureBase

### Delete policy: `delete_policy`

Delete an existing policy.

#### Parameters
*policy_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.delete_policy('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Get policy by guid: `get_policy_by_guid`
Retrieve an existing policy

#### Parameters
*policy_guid*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_policy_by_guid('01234567-89ab-cdef-0123-456789abcdef')
```
- - -

### Get policy by name: `get_policy_by_name`
Retrieves an existing policy

#### Parameters
*name*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.get_policy_by_name('some_policy')
```
- - -

### List policies: `list_policies`
Retrieve a list of existing policies

#### Parameters
*none*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.list_policies()
```
- - -


### Upload policy: `upload_policy`
Upload a policy file to the server

#### Parameters
*policy_file_path*

#### Example
```python
wi = webinspect.WebInspectAPI(host)
response = wi.upload_policy('/User/workspace/some_policy.xml')
```
- - -
