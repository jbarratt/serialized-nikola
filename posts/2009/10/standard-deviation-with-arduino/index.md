<!--
.. title: Standard Deviation with Arduino
.. date: 2009/10/24 13:37
.. slug: index
.. tags:
.. link:
.. description:
-->

My brother and I were playing around with Arduinos as part of my epic road trip this summer. He was trying to get a stable temperature reading from a sensor.

The issue was that the sensor was fine, except when it was rapidly transitioning from one temperature to another. For example, if the ambient temperature was 74, and suddenly a can of soda fresh from the fridge was placed on it, you'd get several "transitional readings" (70, 68, 52, 48, ...) until the temperature finally stabilized.

![Delicious Arduino](/images/119421176_e1c82c8298-300x199.jpg "Delicious Arduino")

We talked about various ways of detecting this case, but the most straightforward one seemed to be [Standard Deviation](http://en.wikipedia.org/wiki/Standard_Deviation), which Wikipedia explains much more clearly than I could.

I googled around for sample code or a library and didn't find any. So even if my Google-fu is weak and there are great resources out there, now there's another one.

The basic idea is that we take 10 samples quickly (20 ms apart), figure out the Standard Deviation, and if that's close enough to zero, we can call this a "stable temperature."

The [full code](http://hub.serialized.net/gitweb/?p=arduino.git;a=blob_plain;f=Standard_Deviation/Standard_Deviation.pde;hb=HEAD) is available from [my git repository](http://hub.serialized.net/gitweb/), but here's the core of it:

``` c
  // Gather sample data

  float sampleSum = 0;
  for(int i = 0; i < SAMPLES; i++) {
    s_val[i] = analogRead(TS);
    sampleSum += s_val[i];
    delay(20); // set this to whatever you want
  }
  float meanSample = sampleSum/float(SAMPLES);

  // HOW TO FIND STANDARD DEVIATION
  // STEP 1, FIND THE MEAN. (We Just did.)

  // STEP 2, sum the squares of the differences from the mean

  float sqDevSum = 0.0;

  for(int i = 0; i < SAMPLES; i++) {
    // pow(x, 2) is x squared.
    sqDevSum += pow((meanSample - float(s_val[i])), 2);
  }

  // STEP 3, FIND THE MEAN OF THAT
  // STEP 4, TAKE THE SQUARE ROOT OF THAT

  float stDev = sqrt(sqDevSum/float(SAMPLES));

  // TADA, STANDARD DEVIATION.
  // this is in units of sensor ticks (0-1023)
```


So, hopefully the comments are self-explanatory (when combined with Wikipedia, if you've never seen Standard Deviation before.)

At the end of this block you have 2 useful variables defined: 'meanSample', which is the mean (average) value of all the samples you polled, and 'stDev' -- the standard deviation amongst all the samples.

This allows you to do things like

``` c
if(stDev < TOLERANCE) {
    // reading is stable enough
    fireMissleAt(meanSample);
}
```

An important note about the units -- the Arduino analogRead values are 12 bit, meaning they range from 0-1023.
In general, those numbers will "mean something" to you. Perhaps you can convert them to a temperature as we were doing, or a direction froma  compass, or a position on a pot. I chose to do the math with the numbers in as raw a form as possible. This means that if you have a sensorToTemp() function, you can call that on meanSample, but you'd also want to call that on stDev as well. Make sure to
convert both values into meaningful values for your application. If you just want to know if the measurement is stable, then perhaps just knowing that the (12 bit) version of stDev is over your comfort level is enough.

Along with Standard Deviation came the need to print out some floating point numbers, so I also included some sample code to do that.
It's hard coded to send things to the serial port, but could be easily tweaked to fabricate a return string or print somewhere else.

``` c
// This is a utility function for printing out floating point values
// Fixed at %0.2f form. (XX.YY, 2 digits after whatever decimal part there is.)
void printFloat(float var) {

  int int_part = int(var);
  int float_part = 100*var - (100*int_part);

  Serial.print(int_part, DEC);
  Serial.print(".");
  if(float_part < 10) {
    Serial.print("0");
  }
  Serial.print(float_part, DEC);
}
```

Hopefully this helps someone else out. It was fun to write and I'm sure I'll have a use for it someday!

Photo Credit (no that's not me!) 

<div xmlns:cc="http://creativecommons.org/ns#" about="http://www.flickr.com/photos/jeanbaptisteparis/119421176/"><a rel="cc:attributionURL" href="http://www.flickr.com/photos/jeanbaptisteparis/">http://www.flickr.com/photos/jeanbaptisteparis/</a> / <a rel="license" href="http://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA 2.0</a></div>
