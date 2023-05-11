# API Blaster

work in progress...

## What is it?
API Blaster is an API testing tool. It is a request manager built as a wrapper around [Httpie](https://httpie.io/) to make API testing a bit easier by leveraging interfaces you're already familiar with - your terminal, text editor and web browser. Create JSON formatted requests using your favorite IDE/text editor, run them with API Blaster and view the results in your browser. 

## Installation

Note: Use virtual environment if you don't want this stored globally. This has only been tested with Python 3.9+


1. CD to directory where the repo is saved

2. `pip install .`

## Setup

In order to start using API Blaster you need to tell it where to look for your requests and where to save responses.

1. Create 2 directories somewhere on your computer that is easily accessible: one to save requests and one to save responses.

2. Type `blast` in your terminal to open API Blaster after installing

3. With API Blaster opened type `settings` and press enter. **Note**: API Blaster uses tab completion so you can type `se` then tab to complete.

4. You should see 6 options displayed. Type `Requests Directory` and press enter.

5. Enter the full path to the directory from step 1

6. Now type `Responses Directory` and enter the responses directory you created in step 1.

#### Other Important Settings

API Blaster uses a [Tornado web server](https://www.tornadoweb.org/en/stable/) to display the responses in your browser, which means it will use a port on localhost and has the potential to interfere with other services you might be using like Docker or Node. API Blaster uses port 8050 by default. 

1. Go to the settings menu (see setup section)
2. Type `Port Number` and press enter
3. Enter your new port number
4. API Blaster should display a message that it was updated successfully and may momentarily pause while stopping the server. If it hangs for more than a few seconds pres `ctl + c` to cancel and re-launch API Blaster (working on a fix!)

## Demo

1. Copy the `.env`, `test-get.json` and `test-post.json` files from the sample_requests directory into the requests directory you created from the setup section

2. Start API blaster with `blast` (cd to the installation directory if it wasn't installed globally)

3. You should see `test-get.json` and `test-post.json` displayed. Type either of those into the prompt and press enter

4. The request was sent to a test endpoint included with API Blaster. You should see 2 options:
   1. "View most recent" followed by a url
   2. "View response by filename" followed by a url

5. Copy the "view most recent" URL and paste it into your browser. You should now see a JSON response with some random content displayed.

6. In API Blaster enter the same item from step 3 and your browser will auto-update with a new response. Submit again and it will update once more...


## Usage

coming soon!