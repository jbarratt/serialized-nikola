<!-- 
.. title: Stopping Docker Containers in a hurry
.. slug: stopping-docker-containers-in-a-hurry
.. date: 2015-05-20 21:13:44 UTC
.. tags: 
.. link: 
.. description: 
.. type: text
-->

I've been working with [docker-compose](https://docs.docker.com/compose/) a lot, and it's a really great tool. I can't wait to see what they do with it!

However, I found myself doing a lot of `docker compose stop`, `docker compose start`. Shutting down each container was taking approximately 10 seconds each, which, with my setup, meant waiting about a minute for a shutdown. This was certainly manageable, but also added up quickly.

So what happens when you call `docker stop`? The container's main process is sent a signal, `SIGTERM`. It's then given 10 seconds to do any cleanup it wants/needs to, and then it's sent `SIGKILL` and forcibly killed.

By default, `python` [does nothing when it gets a `SIGTERM`](http://pymotw.com/2/signal/), it has the default signal handler installed (`SIG_DFL`). So, for a simple application, you can turn `SIGTERM` into an immediate quit by just doing:

``` python
import sys
import signal

def handler(signum, frame):
    sys.exit(1)

def main():
    signal.signal(signal.SIGTERM, handler)
    ... your special logic here
```

And that's it! Or so I thought. I started the container:

``` console
$ docker run -d --name shutdown_test shutdown_test
$ time docker stop shutdown test
real    0m10.367s
user    0m0.136s
sys     0m0.007s
```

Not awesome. Checking `docker ps` showed the problem, though:

``` console
$ docker ps                                                               
CONTAINER ID        IMAGE                           COMMAND               
272c68f3206e        shutdown_test:latest            "/bin/sh -c ./test.py... 
```

Docker is actually running `sh` as the primary process, which is launching my python script. This is because of the `CMD` entry I was using in `Dockerfile`.

```
CMD ./test.py
```

This version of `CMD`, as you can see, runs the process under a shell.

Converting to the argument list format fixes this:

```
CMD ["./test.py"]
```

There we go:

``` console
$ docker ps                                                            
CONTAINER ID        IMAGE                           COMMAND            
8e5ef05d5389        shutdown_test:latest            "./test.py"        
```

and finally, we get the shutdown times we deserve.

``` console
$ time docker stop shutdown_test 
real    0m0.341s                 
user    0m0.132s                 
sys     0m0.007s                 
```

It took a bit more work to get all the containers in my docker-compose working. Some containers specified different commands in the `docker-compose.yml` itself, so you can do the same thing there.

``` yaml
badcontainer:
  command: "thescript"
goodcontainer:
  command: ["thescript"]
```

Also, if you're using `cherrypy`, their documentation reveals an important [step for handling signals](https://cherrypy.readthedocs.org/en/3.2.6/refman/process/plugins/signalhandler.html):

``` python
if hasattr(cherrypy.engine, 'signal_handler'):
    cherrypy.engine.signal_handler.subscribe()
```

There are a few containers left which have slow shutdowns, but they are ones I'm grabbing from upstream sources. I'm sure some pull requests will be pending!
