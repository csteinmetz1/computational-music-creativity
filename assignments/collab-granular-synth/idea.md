# The collaborative granular synth

There is a main Pd patch that implements a granular synth. 
We use OSC and a simple HTML/CSS/JS front-end that is hosted via a Python server (let's say Flask).
This interface has two main roles. The first role is to access the user's microphone.
After getting permissions a small snippet of sound will be recorded from the microphone,
and this data will be sent to the Python server and saved to disk. On the interface they will 
have some very simple slider controls. Maybe this will control just the start time of the grain
and the density. We then use the Python server to send an OSC message to the Pd patch for it to
load the new grain file saved from the user. Each user will get an ID when the connect and there
will be a limit to the number of users possible (lets start with 4). That means that there will be 
4 dormant granular synths that can be controlled (to keep the CPU usage under control we may
want each synth to use 8 voices - 8x4=32 voices). By default the user may control the grain they
created, but maybe randomly we shift the messages from one user to control the grain of another user.
Then also, at some random time we will want to update the grain from each user. 

use: pyOSC, Flask, 
Record in JS - https://developers.google.com/web/fundamentals/media/recording-audio?hl=en
https://osc4py3.readthedocs.io/en/latest/userdoc.html#introduction
http://write.flossmanuals.net/pure-data/osc/