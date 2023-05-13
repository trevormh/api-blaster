# API Blaster

work in progress...

## What is it?
API Blaster is a "request manager" for [Httpie](https://httpie.io/) designed make API testing a bit easier by leveraging interfaces you're already familiar with - your terminal, text editor and web browser. Create JSON formatted requests using your favorite IDE/text editor, run them with API Blaster and view the results in your browser.

API Blaster uses the tornado web framework to asynchronously serve responses to your browser. You can view responses side by side in different browser tabs for easy visual comparison, or let API Blaster auto-update so that with each request you make your browser automatically refreshes to display the most recent response.

## Installation

Note: Use virtual environment if you don't want this stored globally. This has only been tested with Python 3.9+


1. CD to directory where the repo is saved

2. `pip install .`

## Setup

In order to start using API Blaster you need to tell it where to look for your requests and where to save responses.

1. Create 2 directories somewhere on your computer that is easily accessible: one to save requests and one to save responses.

2. Type `blast` in your terminal to open API Blaster after installing

3. With API Blaster opened type `settings` and press enter.

4. You should see several options displayed. Type `Requests Directory` and press enter.

5. Enter the full path to the requests directory from step 1

6. Now type `Responses Directory` and enter the responses directory you created in step 1.

#### Other Important Settings

API Blaster uses a [Tornado web server](https://www.tornadoweb.org/en/stable/) to display the responses in your browser, which means it will use a port on localhost and has the potential to interfere with other services you might be using like Docker or Node. API Blaster uses port 8050 by default. If you want to use a different port perform the following steps. 

1. Go to the settings menu (see setup section)
2. Type `Port Number` and press enter
3. Enter your new port number
4. API Blaster should display a message that it was updated successfully and may momentarily pause while stopping the server.

## Demo

API blaster includes a couple of test endpoints and the corresponding request files to call those endpoints.

1. Copy the files from the `samples_requests` directory into the requests directory you created from the setup section

2. Start API blaster with `blast` (cd to the installation directory if it wasn't installed globally)

3. You should see `test-get.json` and `test-post.json` displayed. Type either of those into the prompt and press enter

4. The request was sent to a test endpoint included with API Blaster. You should see 2 options:
   1. "View most recent" followed by a url
   2. "View response by filename" followed by a url

5. Copy the "view most recent" URL and paste it into your browser. You should now see a JSON response with some random content displayed.

6. Each time you execute the same request your browser will update with the most recent response (when accessing the "view most recent" url). 


## Usage

coming soon!