## How to use
1. Go to [releases](https://github.com/unassuming-alt/lovense-sniper/releases)
2. Download the version you need, either windows or linux
3. Crate a folder on your computer and put the zip you downloaded in it
4. Unzip it
5. Run the lvns executable
  - optional: before running the exec, open config.json and add your cookie and the path to your users.txt file. This will make these settings permanent every time you lauch the executable
6. Add the users you want to snipe links from to the users.txt file, simply copy their username (one per row)
7. Make sure you either have Chrome or Chromium installed
8. Click on `Launch Browser` on the ui after setting the cookie and location of the users file
9. Use the `Start` and `Stop` buttons to start and stop the sniper
10. Use the `Quit` button to fully with the program

### How to get the cookie
#### Chrome
1. Open Chrome
2. Go to the [lovenselife](https://lovenselife.com/) site
3. Log in
4. Press f12 on your keyboard
5. On the top bar click on Application (if you don't see it the two arrows like this >> or make the sidebar wider)
6. Click on the arrow next to cookies
7. Click on the tab that should appear `https://lovenselife.com/`
8. Copy the value of the cookie called `lovenseclub`

#### Firefox
1. Open Firefox
2. Go to the [lovenselife](https://lovenselife.com/) site
3. Log in
4. Press f12 on your keyboard
5. On the top bar click on Storage (if you don't see it the two arrows like this >> or make the sidebar wider)
6. Click on the arrow next to cookies
7. Click on the tab that should appear `https://lovenselife.com/`
8. Copy the value of the cookie called `lovenseclub`

## To build your own
To build this program all you need are these `selenium` `beautifulsoup4` `PySimpleGUI` libraries
