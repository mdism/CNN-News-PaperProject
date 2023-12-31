# News On PDF
#### Video:  [On Youtube: https://youtu.be/Ru3h80B-CH0](https://youtu.be/Ru3h80B-CH0)

## Description
My project is an ***interactive News PDF generator***. The program will scrape the CNN news website and will create a PDF copy of the news.
This Application will create a PDF copy of the news published on CNN news portal 📰 as per user selection.
Built with [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), [FPDF2](https://pypi.org/project/fpdf2/), [tabulate](https://pypi.org/project/tabulate/)

step-1: Greeting & Showing News Topics menu
![Screenshot- Project Greeting & Showing News Topics menu](Screenshots/ProjectRun_1.jpg?raw=true " News Topics menu")

step-2: Showing all the headlines for the selected topic
![Screenshot- showing all the headlines for the selected topic](Screenshots/ProjectRun_2.jpg?raw=true "headlines for the selection")

Step3: Successfully complete Response.
![Screenshot- Response from project when successfully completed.](Screenshots/ProjectRun_3.jpg?raw=true "successfully completed message.")

Output file:

![Screenshot- Response from project when successfully completed.](Screenshots/NewsPaper.jpg?raw=true "Output file.")



## Environment Setup
Rename .env file
Please rename "renameThisFile.env" file to ".env" only
The file name should only .env


To setup your environment run the code, first install all the requirements:
```
pip3 install -r requirements.txt
```
Once the requirements are installed. how you can run the code saying the following in the terminal window.
```
python project.py
```

if you want to change the output file name you can do it from .env file
```
OutputFilename = "FilenameYouWant.pdf"
```

## how this works?
When the project starts running it will fetch the **menu items** from the site and display on the terminal.
and will ask you to choose one, by entering its corresponding SrNo.
```

*********** Welcome To "News On Pdf" *********** 
 *********** Get your newspaper copy from CNN: https://edition.cnn.com *********** +----------+---------------+
|   Sr. No | News Menu     |
+==========+===============+
|        1 | US            |
+----------+---------------+
|        2 | World         |
+----------+---------------+
|        3 | Politics      |
+----------+---------------+
|        4 | Business      |
+----------+---------------+
|        5 | Opinion       |
+----------+---------------+
|        6 | Health        |
+----------+---------------+
|        7 | Entertainment |
+----------+---------------+
|        8 | Style         |
+----------+---------------+
|        9 | Travel        |
+----------+---------------+
|       10 | Sports        |
+----------+---------------+
 *********** Enter Sr. No of the corresponding menu item, to tell me what you’ve selected. *********** 
Select News by entering its number: <Your Choose Here>

```

Once you will select any topic from the menu and press enter, the program will go and fetch all the **Headlines** related to that topic from CNN Website.
And all the headlines will be displayed on the terminal like above.
````
Select News by entering its number: 2
*********** Fetching Headline on "World" ***********
+--------+------------------------------------------------------------------------------------------------------------------------------------------+
|   SrNo | News Headlines                                                                                                                           |
+========+==========================================================================================================================================+
|      1 | Canadian wildfire smoke reaches Europe as Canada reports its worst fire season on record                                                 |
+--------+------------------------------------------------------------------------------------------------------------------------------------------+
|      2 | Sierra LeoneâsÂ President Maada BioÂ sworn in hours after election win                                                                 |
+--------+------------------------------------------------------------------------------------------------------------------------------------------+
|      3 | Russian missile attack hits Kramatorsk city center, killing at least four, say Ukrainian officials                                       |
+--------+------------------------------------------------------------------------------------------------------------------------------------------+
 
*********** Enter Sr. No of a corresponding menu item, to tell me what you’ve selected. ***********
Select News by entering its number:

````
You can now select by its headline.
once the corresponding Sr.No is entered for a headline. the PDF file on the root directory will be created as shown in the output file screenshot above.


## Python version Supported
this project is created on ***Python 3.9.16*** python version

## Notes
🚪 Any time if you want to stop the application enter *0(zero)* or *any negative number*.
⚠️ While fetching news details from a website if any unexpected error happens it will inform about the same and ask to try again.
but the error out new will be removed from the menu. 😀
for now, this project only supports CNN news website.

### Disclaimer
# This project is undertaken solely for learning purposes, with no intention to utilize any documents, material or news obtained from any news’s website for reproduction or mination elsewhere.


Feel free to fork if you like to update this project.

## Disclaimer
This project is undertaken solely for learning purposes, with no intention to utilize any documents, material or news obtained from any news’s website for reproduction or mention elsewhere.

