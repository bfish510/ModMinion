#Guide to Running on Linux!

##Overview

This guide is made because I've been in someones shoes who has no idea what to do. Resorting to a ton of unrealted stackoverflow posts that you can't always trust and aren't sure if they work can be a pain for something that should be simple. Here is how I set my enviorment up. It may not be the best but I want to define all the tools I use and why I use them.

##Notes

I'm running this on Ubuntu 14 LTS, if anything need to be mentioned for earlier versions I'll be happy to make note. This version has python 3.4 already installed so we don't need to worry about that. Off to the guide!

##Guide

1. If you are on a windows box and looking to SSH into a server, I recommend Putty or Kitty. Either is fine. This will allow you to use the linux terminal from your windows machine. Once connected to your server, login and let the fun begin!
2. Check the version of Python 3 installed by using the ```python3``` command with no flags. You should see ```Python 3.4.0``` at time or writing.
3. Let's install pip! Pip allows us to install python packages so we can use them in our code and it's dead simple! We will also be using apt-get here which is a package manager for Linux that let's use install cool new programs and all their dependencies! use the command ```apt-get install python3-pip``` to install pip. We need to designate python 3 because python 2 is still actively used. If the command fails try ```sudo apt-get install python3-pip``` since it might be a privledge issue. Sudo allows us to run a command as a super user. It is always good to run programs at the lowest level of privledge possible to prevent security vulnerabilites becomming a bigger issue if a program is hacked or vulnerable. Assume they all are!
4. Now that it's installed, we can use pip. ```pip3 install praw``` will tell the Python 3 version of pip that we want to intall the Python package praw. Praw is used to make calls the the Reddit api.
5. Next, I use the ```screen``` command to switch to another terminal. This is done so that we can run our program from this terminal and exit it without forcing the program to shut down beause the terminal recieved an interupt. ```nohup``` is another option but I have more experience using ```screen```.
6. Let's run the program! If everything was done correctly, you should be able to run ```python3 ModMinion.py``` and have it ask for credentials. After following the startup process, use ```ctrl-a``` then ```ctrl-d``` or just ```d``` to return to the original terminal.
7. Enjoy!

##Tools

Putty - Used to ssh into a linux box.
Kitty - another Windows SSH tool. 
Python 3.4 - the version of python we are using to run ModMinion chosen because it comes preinstalled with pip for windows.
Screen - used to create a new terminal so that we don't force our program to exit when we close out terminal.
pip - python package installer
apt-get - Linux package installer

Let me know if I seem to be missing a step or something is wrong! I'm assuming someone using this guide has never used Linux. 
