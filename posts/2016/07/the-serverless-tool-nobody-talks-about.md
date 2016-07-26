<!-- 
.. title: The Serverless Tool Nobody Talks About
.. slug: the-serverless-tool-nobody-talks-about
.. date: 2016-07-25 22:43:28 UTC
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

I'm a big fan of the recent rise of "Serverless" computing, spearheaded by AWS's Lambda. Many people have pointed out that "Serverless is made of servers", which is a fair point. ("Functions as a Service" is probably better.) But they aren't servers that I have to pay for when I'm not using, keep patched, manage runtimes for, and so on. There are obviously tons of use cases where FaaS won't work -- but when it will, why not?

It hit me the other day, though, that I've used another tool that lets code be written and run -- even sophisticated use cases like running on a schedule, interacting with other web services, and so on -- which vastly predates AWS Lambda. That tool is Google Apps Script.

Here's a problem I had been thinking of solving with Lambda (mostly as an exercise in building an end-to-end app, but also because it was a real problem I had.)

My kids get allowance: $1/week for every year old they are.
We still want them to physically get the funds, so they can have the tangible reality of collecting it, having to give it back when they buy things they've saved for, and allocate between Spend/Save/Give categories.

The problem is, I had a terrible track record of remembering to hand it out on our typical period. And a lot of the time I did remember, it coincided with a lack of small bills or coins.

What I needed was a system which would 'buffer' for me. The desired features were:

* Deposit a kid-appropriate number per week
* Allow me to decrement it when "paying out" -- and properly secured, so that nefarious parties (or creative hacker inclined 7 year olds) could not tweak the balances
* Allow the older kids to have read-only views of the values that they could consult via the web. (Desktop bookmarks on iOS.)
* Have an audit trail of when and what changes were made.

I sketched this with Lambda. All very possible, but non-trivial.

* Data could be stored in DynamoDB, or even -- given the low write volume -- as structured data in S3.
* Auth is still a little complicated, even if you using Cognito, but could be linked to Google or Facebook, or even tied to a simple token stored in KMS.
* Read-only access is simple, if publishing the values to a s3 website-enabled bucket.
* Editing could be a pretty simple Single Page App, hosted in the bucket, that targeted an API Gateway endpoint.
* Periodically incrementing the values is also easy, with a scheduled Lambda task.
* The audit trail could be stored in DynamoDB or Cloudwatch Logs.

So it's very doable, but that's also a lot of overhead. If I wanted to build a SaaS allowance product, though, it could be a pretty excellent starting point, with a pretty incredible scaling/cost profile!

However, here's what it took in Google Apps.

* Create a new spreadsheet.
* Set up the basic structure of the document

<div style="max-width:400px;padding-left:20px;">
    <img alt="Spreadsheet" style="max-width:100%;" src="/images/serverless_google/01_sheet.png"/>
</div>


* Launch the script editor (Tools &gt; Script Editor)

<div style="max-width:400px;padding-left:20px;">
    <img alt="Launch Script Editor" style="max-width:100%;" src="/images/serverless_google/02_script_editor.png"/>
</div>

* Enter the simple code

<div style="max-width:400px;padding-left:20px;">
<img alt="Code Listing" style="max-width:100%;" src="/images/serverless_google/03_code_listing.png"/>
</div>

In copy/paste compatible form:

    function divvyAllowance() {
        var ss = SpreadsheetApp.getActiveSpreadsheet();
        for (var i = 2; i <= 4; i++) {
            incby = ss.getRange('B' + i).getValue();
            balance = ss.getRange('C' + i);
            balance.setValue(balance.getValue() + incby);
        }
    }

* Click the 'clock' icon in the script editor to enter the schedule, and set the function to run weekly.


<div style="max-width:400px;padding-left:20px;">
    <img alt="Schedule" style="max-width:100%;" src="/images/serverless_google/04_schedule.png"/>
</div>

And that is it! It meets all the requirements, at no additional cost -- in fact, no cost at all, in many Google plans.

* I can use the Google Sheets app to check on the values if I'm being consulted about a kid's current balance while in a store.
* I can share write access with my wife, too.
* I can give the kids read-only URLs to consult if need be
* The sheets Revision History will track every edit, including the automated ones.

So, of course, this provides far lower control, customization, and possibly even scalability as the full-bore serverless implementation outlined above. But it's also VASTLY more simple and manageable. So, thanks Google, for being Serverless pioneers, and still being a good option for a lot of these use cases!
