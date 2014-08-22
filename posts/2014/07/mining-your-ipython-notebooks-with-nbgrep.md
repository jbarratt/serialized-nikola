<!-- 
.. title: Mining your IPython Notebooks with nbgrep
.. slug: mining-your-ipython-notebooks-with-nbgrep
.. date: 2014-07-23 23:08:00 UTC
.. tags: 
.. link: 
.. description: 
.. type: text
-->

One of the things I like most about [IPython Notebook](http://ipython.org/notebook.html) is right there in the name -- it's a great notebook. Often I'll figure out how to do something, be it talk to a certain API, format a graph in a particular way, parse a certain kind of file, and so on, in one of my notebooks.

The problem is this: I have notebooks in lots directories around my machine. Each data collection/analysis project has it's own repository. I've got notebooks that go with presentations, notebooks for blog posts, a general playground direcory.... you get the idea. So, I'll often remember *that* I solved a particular problem in the past, but not *where* I solved it.

The second problem is that grep and [ack](http://beyondgrep.com/) don't work well with `.ipynb` files.

1. They're not normal line-oriented text, they're JSON files.
2. They don't just have the code; they have your text, but more distractingly, they have the output files, many of which might be SVG or base64 encoded images, large HTML tables, etc.

I found a [useful techique](https://gist.github.com/mlgill/5c55253a3bc84a96addf) from [Michelle Gill](http://themodernscientist.com/) that helps address this second problem. Using [`jq`](http://stedolan.github.io/jq/), a command line JSON processor, you can pick out only the code cells.

```bash
$ jq '.worksheets[].cells[] | select(.cell_type=="code") | .input[]' MyFile.ipynb
```

Great! Now I just need to find all the notebooks. Since I'm on OSX, I know that Spotlight knows where all my .ipynb files are, and I can access that from the CLI with `mdfind`.

```bash
$ mdfind -onlyin ~/work -name '.ipynb'
```

**Update**: Thanks to [Thomas Spura](https://twitter.com/ThomasSpura) for the [fork](https://gist.github.com/tomspur/3e9d9190a8dea097a919), this now works on linux with `find` if you don't have mdfind; I updated [the original gist](https://gist.github.com/jbarratt/fa1d3473048e5f856aeb).

Bolting those ideas together, and I have the very useful script [nbgrep](https://gist.github.com/jbarratt/fa1d3473048e5f856aeb). So if I want to find the notebook I was playing around with the Twitter API in, it's an `nbgrep twitter` away. (Bonus: in the terminal, you even get python syntax highlighting.)

```bash
$ nbgrep twitter

/Users/jbarratt/work/notebookcookbook/Tweet Relief.ipynb:

import twitter
auth = twitter.oauth.OAuth(creds['access_token'], 
twitter_api = twitter.Twitter(auth=auth)
search_results = twitter_api.search.tweets(q='#oscon', count
    search_results = twitter_api.search.tweets(**kwargs)
```
