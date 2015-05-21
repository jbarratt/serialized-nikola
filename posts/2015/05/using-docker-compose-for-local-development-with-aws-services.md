<!-- 
.. title: Using docker-compose for local development with AWS services
.. slug: using-docker-compose-for-local-development-with-aws-services
.. date: 2015-05-21 22:31:43 UTC
.. tags: 
.. link: 
.. description: 
.. type: text
-->

I [previously blogged](/2015/05/stopping-docker-containers-in-a-hurry/) about being frustrated enough with slow docker stop times that I figured out how to speed them up.

I ran into that issue while using `docker-compose` to build an application which used several AWS services. While it's easy enough to develop 'live' against AWS, if it *was* possible to do it locally, it seemed worth doing.

I've uploaded a small ['hello world' repo](https://github.com/jbarratt/docker-compose-fake-aws) to Github, so for TL;DR purposes, take a look!

### The Goals

Ultimately, I want to have a container that I can ship (without alteration) to AWS, while being able to develop and test locally.

On AWS, I will be using [Cloudformation](http://aws.amazon.com/cloudformation/) to apply [EC2 IAM Roles](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) to the production hosts.

This goal led to, for example, only using S3 over SSL, as that's the only way it now works in production.

### "Hello AWS World"

The [script that runs](https://github.com/jbarratt/docker-compose-fake-aws/blob/master/democontainer/demo/demo.py) in the demo container does the following:

1. Connect to s3 and SQS
2. Send a 'Hello World!' message to SQS
3. Read that message back from SQS
4. Store the contents of that message in an S3 bucket.

Clearly this code is not going to be the backbone of the next hot startup, but it demonstrates the end-to-end workflows without too much extraneous code.

And, meeting the goal ✓, the exact same script (or the whole Docker container) runs without alteration on AWS. (Provided the queue and buckets exist, and it has permissions, of course.)

To see it in action, run

``` console
$ docker-compose up -d
```

To see what happens at startup, you can run `docker-compose logs`. You should see all the containers starting up, and the demo process logging:

``` console
$ docker-compose logs
Attaching to dockercomposefakeaws_demo_1, dockercomposefakeaws_fakesqs_1, dockercomposefakeaws_fakes3ssl_1, dockercomposefakeaws_fakes3_1
demo_1      | INFO:aws_demo:Sending message
demo_1      | INFO:aws_demo:Receive the message
demo_1      | INFO:aws_demo:Got message <Hello World!>
demo_1      | INFO:aws_demo:Storing contents into s3 at hello.txt
```

### Docker-Compose

`docker-compose` is an ideal tool for setting this up, as I can create one compose file for production, and another one for local dev. The production file will just be the container(s); the dev/test will also include the mock services.

The whole dev file is [on github](https://github.com/jbarratt/docker-compose-fake-aws/blob/master/docker-compose.yml), and it defines 4 containers:

* `demo`: A demo container that runs a 'hello world' python app
* `fakesqs`: a fake SQS service, powered by the SQS-compatible [ElasticMQ](https://github.com/adamw/elasticmq) (Scala and Akka)
* `fakes3`: A fake s3 service, running the [fake-s3](https://github.com/jubos/fake-s3) ruby gem
* `fakes3ssl`: An nginx-powered SSL proxy to provide SSL to `fakes3`.

This polyglot stack is a great example of how powerful Docker can be. Outside of putting the container names in the configuration file, I had to do zero work to run 4 services that are running completely different languages and tools. Sweet.

One notable 'hack' is in working with the endpoints.

``` yaml
links:                                    
  - fakesqs:us-west-2.queue.amazonaws.com 
  - fakes3ssl:testbucket.s3.amazonaws.com 
```

Docker's `link` feature actually sets up local hostfile entries for the pairs listed here.
So when the code tries to connect to `testbucket.s3.amazonaws.com`, it's going to get the IP for the `fakes3ssl` container instead of the actual AWS endpoint. 

If you're using python, boto has another way to manage this (`BOTO_ENDPOINTS`), but the hostname based approach has the advantage of working with nearly every tool which can work with aws, including `awscli`.

### In-container integration testing

The final neat application of this approach is being able to run full integration tests against these mock services. There is a [simple test file](https://github.com/jbarratt/docker-compose-fake-aws/blob/master/democontainer/demo/tests/test_demo.py) in the repo which just validates that, in fact, 'Hello World!' has been written to `hello.txt` in our bucket.

Again, these tests would work on production AWS if we wanted to ensure that the fake services were *really* equivalent, as they just use the same environment variables for configuration.

The [`Makefile`]() has a useful technique for running a command in a running container attached to a fully configured `docker-compose` stack:

``` console
.PHONY: test

test:
        docker exec -ti `docker ps -q -f 'name=_demo_'` py.test
```

So this finds the running container which has `_demo_` in the name, and runs `py.test` in it.

``` console
$ make test
======================= test session starts ========================
platform linux2 -- Python 2.7.6 -- py-1.4.27 -- pytest-2.7.1
rootdir: /demo, inifile: 
collected 1 items 

tests/test_demo.py .

===================== 1 passed in 0.09 seconds =====================
```

(Normally I would use the `$(docker...)` invocation, but the default shell for `make` doesn't like it, even if I manually set it to `bash`. So, backticks work.)

### Conclusion

Once you figure out some of the quirks of mocking AWS services on AWS, it's incredibly powerful. For some services, AWS even offers official local versions (like [DynamoDB Local](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html), which has of course [already been dockerized](https://github.com/trayio/dynamodb-local)).

Since the environment is self-contained, not only does this speed up (and cost down) local development, but it means we can even integration test AWS-inclusive solutions as part of a CI process.

(BTW, credit for figuring out some of this plumbing goes to my stellar co-workers Dan Billeci and Nate Jones. Thanks guys, it's great working with you!)
