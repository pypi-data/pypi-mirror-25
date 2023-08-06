# Harbor &middot; [![Build Status](https://travis-ci.org/srishanbhattarai/Harbor-CLI.svg?branch=dev)](https://travis-ci.org/srishanbhattarai/Harbor-CLI)

Harbor-CLI is a tool to share Android builds of React Native projects. 

With an intuitive CLI for developers, and a simple but _effective_ mobile app for clients and QAs, you won't have to deal with the hassle of building and deploying your awesome React Native projects again.

_(Note: This repo houses only the CLI for Harbor. The mobile app lives in a [different repo](https://github.com/srishanbhattarai/Harbor).)_

## Requirements
* A linux or macOS/OSX system (Windows compatibility has never been checked and never will be)
* Python 3.3, 3.4, 3.5 or 3.6 

_Python 2 is unsupported._

## Installation
You can install harbor with `pip`.

```
pip install harbor-cli
```
This makes available a `harbor` CLI command. You can run `harbor --help` to see supported commands or see below for usage instructions.

## Workflow
How does the deployment process for a React Native app look like?
  1. For the first time, you need to register your project. Run `harbor register`. That's it.
  2. Invite people to your project using `harbor invite [registeredEmail]`.
    * You can supply a `role` option using `--role=[role]`. Currently, 'dev', 'uat', 'qa' are supported. This falls back to dev if unspecified.
  3. Deploy your project using `harbor deploy`. Easy.
    * You can supply a `type` option using `--type=[releaseType]`. Currently, 'dev', 'uat', 'qa' are supported. This falls back to dev if unspecified and determines how push notifications are sent to users.
    For example, a 'dev' release will be sent to only people invited under the 'dev' role.

Harbor comes out of the box with limited support for [Hipchat](https://www.hipchat.com/sign_in) notifications. To configure this, you need a `harborConfig.json` config file in the root of your project. (Support for more
messaging providers is planned!)

## Motivation
Why did I create this?

Because I like getting stuff done through the CLI, and I didn't find a tool that did it without hassle.
Also, just to have fun. :smiley:

## Contributing
There are a lot more features planned for coming releases! If you'd like to contribute, or pitch in ideas - contact me at my email. :smiley:

Additionally, there are several things I'd like to improve or refactor about the current codebase (better tests being one of them) - but simply do not have the time to do at the pace I'd like. Send in a pull request if you're interested!
