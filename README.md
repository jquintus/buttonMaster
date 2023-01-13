# buttonMaster

The code running the box of buttons on my desktop.

This is running on the [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062). To make it work you'll want to download the latest build of [Circuit Python](https://circuitpython.org/board/feather_nrf52840_express/)

This code is either configured to run off of a [Adafruit NeoTrellis](https://www.adafruit.com/product/3954) or against my custom set of arcade buttons. It's a bit of a manual thing to switch between the two at this point.

## Debugging

For help debugging, see my blog post about using [Circuit Python](https://quintussential.com/archive/2020/06/14/Day-11-Progress-with-Circuit-Python/).

## Checking the code out onto a new device

One option is to just download the code and copy it to the device. Another option is to checkout the code on the device. The problem is that you can't just `git clone https://github.com/jquintus/buttonMaster.git` because the folder already exists. To get around this first delete everything in the root of the drive. Then execute the following git commands.

```
git init
git remote add origin https://github.com/jquintus/buttonMaster.git
git fetch
git checkout origin/main -ft
```
