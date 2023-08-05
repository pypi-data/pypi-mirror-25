<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Quick Start</a>
<ul>
<li><a href="#sec-1-1">1.1. Installation</a></li>
<li><a href="#sec-1-2">1.2. Install specific version</a></li>
<li><a href="#sec-1-3">1.3. Usage</a></li>
</ul>
</li>
<li><a href="#sec-2">2. Overview</a>
<ul>
<li><a href="#sec-2-1">2.1. cf-boot components</a></li>
<li><a href="#sec-2-2">2.2. Architecture diagram</a></li>
<li><a href="#sec-2-3">2.3. Benefits</a></li>
</ul>
</li>
<li><a href="#sec-3">3. Project Spec specification</a>
<ul>
<li><a href="#sec-3-1">3.1. Jobs</a></li>
<li><a href="#sec-3-2">3.2. Spec file</a></li>
<li><a href="#sec-3-3">3.3. Job execution order</a></li>
</ul>
</li>
<li><a href="#sec-4">4. Subscripts</a>
<ul>
<li><a href="#sec-4-1">4.1. Built-in subscripts</a></li>
<li><a href="#sec-4-2">4.2. Creating a new sub-script</a></li>
<li><a href="#sec-4-3">4.3. Adding custom subscripts to the cf-boot path</a></li>
<li><a href="#sec-4-4">4.4. Subscript environment variables, proxies</a></li>
</ul>
</li>
<li><a href="#sec-5">5. FAQ</a>
<ul>
<li>
<ul>
<li><a href="#sec-5-0-1">5.0.1. What happens if a cf-boot invocation fails with jobs left to run?</a></li>
<li><a href="#sec-5-0-2">5.0.2. Is it possible to run a partial set of jobs? Is it possible to "undo" a job?</a></li>
<li><a href="#sec-5-0-3">5.0.3. What if I'm behind a proxy?</a></li>
<li><a href="#sec-5-0-4">5.0.4. Can I bootstrap several environments at the same time?</a></li>
</ul>
</li>
</ul>
</li>
<li><a href="#sec-6">6. Bugs, features</a></li>
</ul>
</div>
</div>

**cf-boot** is a utility to automate the bootstrap process of cloudfoundry
products. It allows users to specificy a product's dependencies
declaratively, and provides a consistent,
reproducible, automated way to bootstrap or update an environment.

# Quick Start<a id="sec-1" name="sec-1"></a>

## Installation<a id="sec-1-1" name="sec-1-1"></a>

    $ pip install --user cf-boot
    $ cf-boot -h
     usage: cf-boot [-h] [-i INPUT] [-o OUTPUT] [-f] [-p PATH]
                    [-g DEPENDENCY_GRAPH_PDF] [-v VERBOSE] [-s]
                    project-spec
     ...

## Install specific version<a id="sec-1-2" name="sec-1-2"></a>

    $ pip install --user cf-boot==1.6.0 --force-reinstall

Or from the source tree (not recommended):

    $ git clone https://github.build.ge.com/hubs/cf-boot
    $ cd cf-boot
    $ sudo python setup.py install

## Usage<a id="sec-1-3" name="sec-1-3"></a>

    $ cf-boot ui-app-hub-boot.json -i envs/hubs-poc.json -o hubs-poc-results.json

-   Obtain or create the project spec: [event-hub-boot.json](doc/examples/event-hub/event-hub-boot.json)
-   Determine the free variables for the project spec
    
        cf-boot event-hub-boot.json --free-vars
        [
           "CF_ORG",
           "CF_PASSWORD",
           "CF_SPACE",
           "CF_SPACE_UAA",
           "CF_TARGET",
           "CF_USER",
           "event-hub-instance-name",
           "event_hub_publish_client_id",
           "event_hub_publish_client_secret",
           "event_hub_subscribe_client_id",
           "event_hub_subscribe_client_secret",
           "uaa_admin_secret",
           "uaa_instance_name"
        ]
-   Create a file: `envs/hubs-poc.json` initializing all free variables
    
        {
            "CF_TARGET": "https://api.system.asv-pr.ice.predix.io",
            "CF_USER": "ernesto.alfonsogonzalez@ge.com",
            "CF_PASSWORD": "***REMOVED***",
            "CF_ORG": "HUBS",
            "CF_SPACE": "poc",
            "CF_SPACE_UAA": "sandbox",
        
            "event-hub-instance-name": "event-hub-audit-poc",
            "uaa_instance_name": "event-hub-audit-uaa-poc",
            "uaa_admin_secret": "ernesto",
        
            "event_hub_subscribe_client_id": "eh-subscribe",
            "event_hub_subscribe_client_secret": "eh-subscribe-secret",
        
            "event_hub_publish_client_id": "eh-publish",
            "event_hub_publish_client_secret": "eh-publish-secret"
         }
-   Run jobs to bootstrap the environment.
    
        $ cf-boot event-hub-boot.json --input envs/hubs-poc.json --output envs/hubs-poc-results.json
        ...
        RUNNING CHILD 3/5: 'service' with input:
        {
          "service": "predix-uaa",
          "instance_name": "event-hub-audit-uaa-poc",
          "cf_home": "/tmp/cf-homes/fafe452c36298bad655f458cdd96a149",
          "plan": "Tiered",
          "credential_paths": {
            "issuerId": [
              "issuerId"
            ],
            "uri": [
              "uri"
            ],
            "zoneId": [
              "zone",
              "http-header-value"
            ]
          },
          "payload": {
            "adminClientSecret": "mysecret"
          }
        }
        
        ...
        
        {
          "issuerId": "https://fe5540ee-d75d-4d9a-8898-9ba9f6de29f5.predix-uaa.run.asv-pr.ice.predix.io/oauth/token",
          "zoneId": "fe5540ee-d75d-4d9a-8898-9ba9f6de29f5",
          "uri": "https://fe5540ee-d75d-4d9a-8898-9ba9f6de29f5.predix-uaa.run.asv-pr.ice.predix.io",
          "SERVICE_GUID": "fe5540ee-d75d-4d9a-8898-9ba9f6de29f5"
        }
        
        ...
-   View bootstrap results: `cat envs/hubs-poc-results.json`
    
         {
          "CF_HOME": "/tmp/cf-homes/1479497b751ec97462bb89660c4962a8",
          "CF_HOME_UAA": "/tmp/cf-homes/fafe452c36298bad655f458cdd96a149",
          "CF_ORG": "HUBS",
          "CF_PASSWORD": "***REMOVED***",
          "CF_SPACE": "poc",
          "CF_SPACE_UAA": "sandbox",
          "CF_TARGET": "https://api.system.asv-pr.ice.predix.io",
          "CF_USER": "ernesto.alfonsogonzalez@ge.com",
          "event-hub-instance-name": "event-hub-audit-poc",
          "event_hub_instance_guid": "a06b5b4c-981a-4f86-84e8-c08f4d2d05e0",
          "event_hub_publish_client_id": "eh-publish",
          "event_hub_publish_client_secret": "***REMOVED***",
          "event_hub_scope_publish_grpc": "predix-event-hub.zones.a06b5b4c-981a-4f86-84e8-c08f4d2d05e0.grpc.publish",
          "event_hub_scope_publish_wss": "predix-event-hub.zones.a06b5b4c-981a-4f86-84e8-c08f4d2d05e0.wss.publish",
          "event_hub_scope_subscribe_grpc": "predix-event-hub.zones.a06b5b4c-981a-4f86-84e8-c08f4d2d05e0.grpc.subscribe",
          "event_hub_scope_user": "predix-event-hub.zones.a06b5b4c-981a-4f86-84e8-c08f4d2d05e0.user",
          "event_hub_subscribe_client_id": "eh-subscribe",
          "event_hub_subscribe_client_secret": "***REMOVED***",
          "uaa_admin_secret": "***REMOVED***",
          "uaa_instance_guid": "fe5540ee-d75d-4d9a-8898-9ba9f6de29f5",
          "uaa_instance_name": "event-hub-audit-uaa-poc",
          "uaa_issuer_id": "https://fe5540ee-d75d-4d9a-8898-9ba9f6de29f5.predix-uaa.run.asv-pr.ice.predix.io/oauth/token",
          "uaa_uri": "https://fe5540ee-d75d-4d9a-8898-9ba9f6de29f5.predix-uaa.run.asv-pr.ice.predix.io",
          "uaa_zone_id": "fe5540ee-d75d-4d9a-8898-9ba9f6de29f5"
        }

# Overview<a id="sec-2" name="sec-2"></a>

## cf-boot components<a id="sec-2-1" name="sec-2-1"></a>

-   **project spec** (`what`)
    -   User-provided specification of the bootstrap requirements:
        A JSON DSL specifying a set of `jobs`,
        each of which specifies
        -   the script to execute it
        -   the inputs to the script
        -   the outputs to capture from the script
        
        Outputs from one job can be passed as inputs to another job
    -   **free variables** (`what`)
        -   environment-specific values or sensitive values such as passwords
            or other credentials, which are decoupled from the project spec
-   **subscripts** (`how`)
    -   Executable, reusable scripts that are invoked
        by the master script to carry out a job
        specified in the user's project spec.
-   **master script** (`what` + `how`)
    -   project-spec parsing and execution engine, organizing jobs by dependency,
        piping job inputs and outputs, producing final JSON key-value map  
               The master script links the `what` and the `how`

## Architecture diagram<a id="sec-2-2" name="sec-2-2"></a>

![img](cfboot/master/hubs-bootstrapper-architecture.png "Architecture diagram")

## Benefits<a id="sec-2-3" name="sec-2-3"></a>

-   Decoupling of `how` and `what` allows users to bootstrap
    their products declaratively instead of writting code
-   Arbitrary chaining of jobs and the data they produce
-   Automatic dependency management based on inputs/outputs
-   Decoupling of environment-specific values, credentials, passwords from the
    project spec
    -   Allows project spec to be published and serve as bootstrap documentation
    -   Allows project spec to remain stable across environments
-   Flexibility to allow user to provide custom subscripts
    to meet highly product-specific bootstrap needs
-   Idempotence as a way to cleanly address the need to update,
-   Idempotence as a way to handle or clean up undefined or undesirable state

# <a id="project-spec" name="project-spec"></a> Project Spec specification<a id="sec-3" name="sec-3"></a>

The project spec is a JSON document

## Jobs<a id="sec-3-1" name="sec-3-1"></a>

A job is a JSON map with 3 required fields, **script**, **input**, **output**, and optionally a **description**

<table border="2" cellspacing="0" cellpadding="6" rules="all" frame="border">


<colgroup>
<col  class="left" />

<col  class="left" />

<col  class="left" />

<col  class="left" />
</colgroup>
<tbody>
<tr>
<td class="left">**field name**</td>
<td class="left">**field type**</td>
<td class="left">**field description**</td>
<td class="left">**example**</td>
</tr>


<tr>
<td class="left">script</td>
<td class="left">string</td>
<td class="left">the name of the sub-script to carry out the job</td>
<td class="left">"create-uaa-service"</td>
</tr>


<tr>
<td class="left">output</td>
<td class="left">map of string -> string</td>
<td class="left">keys much match sub-script output names. values are the names that other jobs may refer to.</td>
<td class="left">{"service\_guid":"uaa\_service\_guid", "client\_secret":"uaa\_client\_secret", "uaa\_uri":"uaa\_uri"}</td>
</tr>


<tr>
<td class="left">input</td>
<td class="left">map of string -> JSON</td>
<td class="left">keys must match sub-script input names. values may be any JSON object. nested strings starting with `$` are substituted with their known value</td>
<td class="left">{"uaa\_uri":"$uaa\_uri", "uaa\_client\_secret":"$uaa\_client\_secret", "acs\_zone":"$acs\_zone"}</td>
</tr>


<tr>
<td class="left">description</td>
<td class="left">string</td>
<td class="left">optional description of the job</td>
<td class="left">"uaa service for config manager"</td>
</tr>
</tbody>
</table>

## Spec file<a id="sec-3-2" name="sec-3-2"></a>

A spec file is a JSON mapping "jobs" to a list of jobs:

    {
       "jobs": [
    ...
          {
             "script": "create-unique-cf-home",
             "description": "unique cf login for all sub-scripts that must use cf commands",
             "input": {
                "CF_TARGET": "$CF_TARGET",
                "CF_USER": "$CF_USER",
                "CF_PASSWORD": "$CF_PASSWORD",
                "CF_ORG": "$CF_ORG",
                "CF_SPACE": "$CF_SPACE"
             },
             "output": {
                "CF_HOME": "CF_HOME"
             }
          },
          {
            "script": "service",
            "description": "create event hub uaa",
            "input": {
                "instance_name": "$uaa_instance_name",
                "service": "predix-uaa",
                "plan": "Tiered",
                "cf_home": "$CF_HOME",
                "payload": {"adminClientSecret": "$uaa_admin_secret"},
                "credential_paths": {"uri" : ["uri"],
                                     "issuerId": ["issuerId"],
                                     "zoneId": ["zone", "http-header-value"]}
            },
            "output": {
                "SERVICE_GUID": "uaa_instance_guid",
                "uri": "uaa_uri",
                "issuerId":  "uaa_issuer_id",
                "zoneId": "uaa_zone_id"
            }
        },
        {
            "script": "service",
            "description": "create event hub instance",
    
            "input": {
                "instance_name": "$event-hub-instance-name",
                "service": "predix-event-hub",
                "plan": "Beta",
                "cf_home": "$CF_HOME",
                "payload": {"trustedIssuerIds": ["$uaa_issuer_id"]},
                "credential_paths": {"event_hub_scope_user":
                                     ["publish", "protocol_details", 0, "zone-token-scope", 0],
    
                                     "event_hub_scope_publish_grpc":
                                     ["publish", "protocol_details", 0, "zone-token-scope", 1],
    
                                     "event_hub_scope_publish_wss":
                                     ["publish", "protocol_details", 1, "zone-token-scope", 1],
    
                                     "event_hub_scope_subscribe_grpc":
                                     ["subscribe", "protocol_details", 0, "zone-token-scope", 1]
                                    }
            },
            "output": {
                "SERVICE_GUID": "event_hub_instance_guid",
                "event_hub_scope_user": "event_hub_scope_user",
                "event_hub_scope_publish_grpc": "event_hub_scope_publish_grpc",
                "event_hub_scope_publish_wss": "event_hub_scope_publish_wss",
                "event_hub_scope_subscribe_grpc": "event_hub_scope_subscribe_grpc"
            }
        }
    
          ...
        ]
    }

-   In the first job
    -   `$CF_TARGET`, `$CF_USER`, `$CF_PASSWORD`, `$CF_ORG`, `$CF_SPACE` are free variables since they are not produced by any other job.
    -   `create-unique-cf-home` script outputs a variable `CF_HOME`, which we capture internally as `CF_HOME`
-   The second job
    -   refers to the `$CF_HOME` produced by the first job
    -   Its script outputs a variable `SERVICE_GUID`,
        which we capture internally as `uaa_instance_guid`
-   The third job uses `uaa_instance_guid` from the second job, as
    well as `CF_HOME` from the first job, and produces `event_hub_instance_guid`

A project spec is malformed if it contains two jobs which output the same
variable

## Job execution order<a id="sec-3-3" name="sec-3-3"></a>

The master script automatically determines job order based on variable dependencies. If
-   Job **A** outputs **X** and
-   Job **B** refers to **$X**, then
-   Job **A** must run before Job **B**

This implies no job can depend on a job that produces no outputs.
For such cases, a job may produce a dummy indicator variable that can be refered by any dependent jobs.  

A project spec is malformed if it contains cyclic job dependencies

# Subscripts<a id="sec-4" name="sec-4"></a>

## Built-in subscripts<a id="sec-4-1" name="sec-4-1"></a>

The following subscripts are provided by default as basic cf bootstrapping
building blocks:

-   [create-unique-cf-home](cfboot/scripts/create-unique-cf-home)
    -   Allows other subscripts to call cf commands against a
        particular environment safely
    -   Allow jobs to target different environments simultaneously without
        conflict
-   [service](cfboot/scripts/create-service),
    -   create or update a service, and optionally extract some of its binding
        credentials by specifying each credential's JSON path
-   [cf-cups](cfboot/scripts/cf-cups)
    -   create or update a user-provided service service
-   [cf-push-app](cfboot/scripts/cf-push-app)
    -   push an app based on a git url. optionally specify services to bind,
        environment variables, route domain name, buildpack, etc
-   [create-uaa-clients](cfboot/scripts/create-uaa-clients)
    -   create or update clients, users, groups on a uaa server
-   [create-acs-policy](cfboot/scripts/create-acs-policy)
    -   create or update an acs policy

## Creating a new sub-script<a id="sec-4-2" name="sec-4-2"></a>

A subscript is any executable file NAME.EXT that conforms to the following requirements:
-   Is executable
-   Lives under `NAME/NAME.EXT` somewhere on the subscripts **path**
-   Read all its input from stdin JSON
-   Output all data as a JSON key-value pairs
    -   May display progress/debug logs to stderr
-   Must be idempotent. Running the script multiple times should be equivalent to running it once
    -   Most of the cf api, as well as cf commands already have this property

Sub-scripts should also observe the following guidelines
-   Have small and clearly defined scope and meaningful name
-   Be self-contained and not interfere with OS user or other processes
    -   Any scripts running CF commands must explicitly set the CF\_HOME environment variable
    -   Should not use uaac until CF\_HOME-like support is added

Pull requests are welcome for subscripts which meet the above guidelines
and provide functionality not already covered

## Adding custom subscripts to the cf-boot path<a id="sec-4-3" name="sec-4-3"></a>

Use the `--path` flag to specify the custom subscript's directory:

     $ cf-boot -h
     ...
    -p PATH, --path PATH  colon-delimited path where to find additional
                           subscripts
     $ cf-boot ui-app-hub-bootstrap.json --path /path/to/my/own/subscripts --input envs/hubs-poc.json
     ...

## Subscript environment variables, proxies<a id="sec-4-4" name="sec-4-4"></a>

The master script's environment variables are passed onto its children subscripts, including https\_proxy.  
   It is up to the subscripts to either use or override these variables.

# FAQ<a id="sec-5" name="sec-5"></a>

### What happens if a cf-boot invocation fails with jobs left to run?<a id="sec-5-0-1" name="sec-5-0-1"></a>

Every subscript is designed to be idempotent, making it safe to re-run the bootstrap.
If a job fails and bootstrap doesn't complete successfully, resolve the problem and re-run the
bootstrap from start until it is successful.

### Is it possible to run a partial set of jobs? Is it possible to "undo" a job?<a id="sec-5-0-2" name="sec-5-0-2"></a>

No. The correct way to resolve an incomplete bootstrap is to fix all problems and re-run from start.

### What if I'm behind a proxy?<a id="sec-5-0-3" name="sec-5-0-3"></a>

Standard proxy environment variables are passed on to cf-boot's subprocesses (subscripts),
which usually know how to interpret them. All the standard subscripts are known to work behind proxy.

### Can I bootstrap several environments at the same time?<a id="sec-5-0-4" name="sec-5-0-4"></a>

By design, the standard subscripts do not persist state, nor do they interfere with concurrent
invocations. Additionally most subscripts rely on a unique, disposable, stateless CF\_HOME login,
on REST calls, etc.
So it should be possible to run the same project spec on the same machine, with different free-vars
inputs.

# Bugs, features<a id="sec-6" name="sec-6"></a>

Submit bug reports or feature requests to cf-boot-devel@ge.com