# Group-4: Visualizing Trends in Email Communication Over Time
### Authors: Casey McGinley, Athanasios Papadopoulos

### Screenshot of the application
![](https://github.com/nyu-cs6313-fall2015/Group-4/blob/master/images/app_scrnshot_20151220.png)

### Description
When government investigators are looking into some party or entity, one of the critical things they need to understand is with whom this party is communicating, to what extent, and how this might have changed over time. To that end, email represents a rich format from which to draw conclusions about the communication patterns of some party or parties. However, when dealing with a large volume of email communications, it is time-consuming and impractical for the investigator to look through individual emails in order to extract the relevant details pertaining to communication trends. Our visualization will address this issue, providing a visual means for the investigator to quickly grasp the aforementioned trends.
<br/><br/>
Our application provides investigators with a timeline of sorts, mapping time (in months) to the x-axis and users (email addresses) to the y-axis. The timeline/chart displayed is always given in the context of a single selected user. The other users on the y-axis are the users that they communicated. On the chart, using area to encode email volume, red nodes indicate emails sent by the selected user and green nodes indicate emails that the selected user received (in other words, the emails sent by to the selected user by the other user). In this way, our visualization allows an investigator tp easily view and understand the variances in communication patterns for a given user.
<br/><br/>
This visualization was created as a final project for the Information Visualization class taught by Prof. Enrico Bertini at the NYU Tandon School of Engineering.

### Video
A video detailing the problem our visualization solves and how our viz can be used can be found below:
* [Video](insert link here)

### Demo
A live demo of this visualization tool is available at:
* [Demo](http://nyu-cs6313-fall2015.github.io/Group-4/)

### Final Report
The final report we compiled, detailing all aspects of this project can be found below:
* [Final Report](https://docs.google.com/document/d/10lqvxBguJ9NJXVSaD6KxuYbIgZnCyyv5ESR23sZV87w/edit?usp=sharing)

### Data
The original, unprocessed dataset can be found below:
* [Raw Data](https://www.cs.cmu.edu/~./enron/)

The significantly smaller and more structured dataset we derived from the above can be found here:
* [Processed Data](https://github.com/nyu-cs6313-fall2015/Group-4/blob/master/data.json)
