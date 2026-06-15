# Globus Notes

## Globus is a high-perfromance file transfer system that is now fully supported in the UW hyak system.

The big deal is that it comes with a web-based file management app that allows drag-and-drop transfers freely across:

- your laptop
- apogee and perigee
- klone
- kopah

It easily and reliably handles huge transfers (many terrabytes!). You simply initiate the transfer in the website, then leave, and it will send you an email when it is done.

---

### Setup

Parker and Kate requested mapping of our UW NetID's to the macc kopah storage account. We did this by sending an email to help@uw.edu with "Kopah + Globus" in the subject line.

Once this is done you have to do a bit more installation, but the documentation in the hyak system is excellent.

#### Globus setup (notes from Kate)
I started here; steps listed below:   
https://hyak.uw.edu/docs/storage/globus/   

Step 1: 1st login
* Go to globus.org and "LOG IN" with University of Washington. Sign in will include Duo 2-Factor Authentication. 
* Using the File Manager - Collection Search tab look for "UW Hyak Klone" and then entered our macc group path, /mmfs1/gscratch/macc/ (needed to click thru 2 onscreen steps to verify my credentials). You should see our files on klone now. Create bookmark once working. 

Step 2: Setting up local endpoint 
* On my laptop, I downloaded Globus connect personal for Mac and followed prompts here: https://docs.globus.org/globus-connect-personal/install/mac/ 
* While configuring your Globus Connect Personal endpoint, be sure to select a unique name for your device (e.g. USER_MacBook_XYZ)
* in globus/file manager, I created a bookmark with my new collection, USER_MacBook_XYZ

Step 3: Setting up an endpoint on apogee 
I followed David Darr's notes (below), but did my download and extract in dat1/kmhewett. 

$  wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
```
tar xzf globusconnectpersonal-latest.tgz
```
this will produce a versioned globusconnectpersonal directory

replace `x.y.z` in the line below with the version number you see
```
cd globusconnectpersonal-x.y.z
```
run this command and follow instructions to setup:
```
./globusconnectpersonal -setup --no-gui
```
You will get a msg like: 
```
Globus Connect Personal needs you to log in to continue the setup process.

We will display a login URL. Copy it into any browser and log in to get a
single-use code. Return to this command with the code to continue setup.

Login here:
-----
GLOBUS-URL-GENERATED-HERE
-----
Enter the auth code:
```
Copy GLOBUS-URL between the dashed lines and paste it into a web browser.  Follow the on screen prompts. This will get you an auth code that you can enter after the terminal prompt. 

Then start (in background): 
```
./globusconnectpersonal -start &
```
check status:

```
./globusconnectpersonal -status
```

At this point I could only see my directory, kmhewett. But by following David Darr's notes, I was able to edit my globus config file: /home/$USER/.globusonline/lta/config-paths (by default globus only sees /home/$USER).  I did not have to create the file, but I edited it so that I could see Parker's directory under dat1. This looks like :

```
~/,0,1
/dat1/kmhewett/,0,1
/dat1/parker/,0,1
```

Then confirmed that I could see these itesm on the file manager at globus.org 


#### perigee or apogee (Notes from David Darr)

Here is how to install this. If you have questions consult https://docs.globus.org/globus-connect-personal/install/linux/ or ask me. I find the online documentation somewhat misleading in a couple of places. Otherwise this is pretty straight forward.

download and extract (I did this in my /dat1/parker directory on apogee, since we try not to put too much in ~):

$  wget https://downloads.globus.org/globus-connect-personal/linux/stable/globusconnectpersonal-latest.tgz
```
tar xzf globusconnectpersonal-latest.tgz
```
this will produce a versioned globusconnectpersonal directory

replace `x.y.z` in the line below with the version number you see
```
cd globusconnectpersonal-x.y.z
```
run this command and follow instructions to setup:
```
./globusconnectpersonal -setup --no-gui
```
start (in background): 
```
./globusconnectpersonal -start &
```
check status:
```
./globusconnectpersonal -status
```
The next step is to edit the file: /home/$USER/.globusonline/lta/config-paths (by default globus only sees /home/$USER).  Note that you might have to create this file (it doesn't always seem to be there by default).

Here, is an example of how this looks on perigee after I added my perigee data directories:

```
more config-paths
```
```
~/,0,1
/data1/darr/,0,1
/data2/darr/,0,1
```
Of course you will need to add your own info here, not David's!

---

### GUI

The next step is to start using the web-based GUI for moving files across systems. This is a lot like a file transfer app like Transmit, but much more powerful. Most importantly it works with klone and kopah as well as your laptio and our servers.

See https://hyak.uw.edu/docs/storage/gui for instructions.


