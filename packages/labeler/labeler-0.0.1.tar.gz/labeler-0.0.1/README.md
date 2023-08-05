# Labeler

[![Build Status](https://travis-ci.org/totalgood/civicu_app.svg?branch=master)](https://travis-ci.org/totalgood/civicu_app/)

Gamify your bot training!

## Description

With this game you can find out if you have what it takes to be a carnivore tracker.

* Can you tell the difference between a coyote and a wolf?
* A mouse and a squirrel?
* At night?
* What about their tracks?
* Are you master tracker material?

And you'll be helping the Cascadia Wild citizen science program by playing our "reindeer games."
The more images you and your friends label, the more data we have about the ecosystem on Mt Hood and nearby forests.

Want to do more than just "play games", upload your own images of Mt Hood wildlife and tracks to answer questions like:

* Did OR-7 spend time near Hood?
* Are there surviving Montagne Fox hiding in some seculeded ravine?
* Will Wolverines ever return to Hood?

And if you can think of other applications for this software, go for it!
You can upload your own images using the [REST API at `/api/images/`](http://localhost:8000/api/images/) or the janky [`/upload` page](http://localhost:8000/upload/).
And since it's fully open science (open source and open data), you can retrieve our labeled images and do whatever you like with them, or modify our code to contribute your ideas.

## Installation

```bash
pip install labeler
```

## Contribute

```
git clone https://github.com/totalgood/civicu_app/
pip install -e civicu_app/
cd civicu_app
python manage.py runserver
```
