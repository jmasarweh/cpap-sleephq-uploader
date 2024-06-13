# cpap-sleephq-uploader
Uploads CPAP data to the SleepHQ Cloud.


Info:

The uploader consists of two main executable python3 files:

-ezshare_downloader_v1.py which will download your cpap files stored on an Ezshare Wifi SD Card plugged in to your machine (credit to: @JCOvergaar https://github.com/JCOvergaar)

-resmed_sleephq_uploader_v2.py which will take the dowloaded files from the first module above, and upload them to https://sleepHQ.com

Prerequisits:

-These files requires libraries and syntaxes written in Python3 (Python 3.9.6 as of this readme was last updated). Download your OS copy accordinly.

-For now these files run based on MacOS directories ie: /User/YourUserFolder/Documents/CPAP_Data/SD_Card/. Create a CPAP_Data folder under your User's Document folder. Then create the SD_Card subfolder under CPAP_Data.

-The ezshare_downloader module will delete anything in the SD_Card and DATALOG folders, so make sure you have backed these up. The deletion occurs to ensure clean fresh data is sent to SleepHQ at each run.

Installation:

Python3
# #################################################################################################
# Setup instructions for Mac users:
#  Install HomeBrew (if you don't have it)
#    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#  Install Python 3 using HomeBrew
#    brew install python
# Install additional libraries using python's package installer
#    pip install requests beautifulsoup4
# #################################################################################################


You will first need to grab your API Keys and Secreats from the SleepHQ Account Settings section/API Keys.

CLIENT_ID -> This is your Client Id from the SleepHQ Account Settings section/API Keys

CLIENT_SECRET -> This is your Client Secret from the SleepHQ Account Settings section/API Keys

DEVICE_ID -> (Placeholder, may not be needed)

SUB_PATH -> This will be the path to your SD_Card folder, i.e "/Users/John/Documents/CPAP_Data/SD_Card" without the last forward slash

DIR_PATH  -> This will be the path to your SD_Card folder, i.e "/Users/John/Documents/CPAP_Data/SD_Card/" WITH the last forward slash


Save the .env file in the same directory of the two py files above.

Important Info:

The modules will only upload the last night's data. It will not upload any prior data. It can be tweaked to handle all the files, but you would need to be realise that for mass uploads, the SleepHQ.com web UI is much faster.

The modules have been tested for the folders and directory structure above. You can have your own paths, as long as the absolute path to the SD_Card folder is consistent with SUB_PATH and DIR_PATH above.

Any tweaks and comments are welcomed.

