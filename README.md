# AWS_cloudformation_python
<h4>Studying US visa application</h4>
The task in spite of coding part also obliged to get to know what kind of data i am preparing for data scientists. It was interesting part to learn about NAICS (North American Industry Classification System) and understand why do we need such system. <br/>
<h4>Challenges&Approaches</h4>
The first challenge was to get to know how my data which i need to prepare looks like. First of all i noticed asymetric distribution of colons comparing the header and the data in the file. I wanted to make this app object-oriented and tried as much as rules of the task were allowing me to make this code reusable taking into cosideration "explicitly over implicitly". So my initial idea was to create method get_header() which would return dictionary where keys will be the attributes and values will be the number of the column to the corresponding attributes. The idea behind this is to analyze similar files and not being worried about if our header attributes will not be in this same order or if in the future there will be added a new attributes... Then easily we will be able to access them by key what is also explained in documentation of this method. During this problem i used methods on strings which would split line by colons and remove unnecessary fields in the list like escape characters e.g. "\n". Next problem was the way of parsing file... Once i thought about read() method however it would be a very bad decision just in case if our file would be so much bigger, it could turn out as "bottleneck" in my program. That's why it is better to parse data in chunks whch may be more effective with use of such modules like e.g. Pandas or Dask. Another problem was handling multiple occupations per NAICS_CODE. Didn't want to lose such data so i created additional data structures for extra occupations per NAICS_CODE which appears
after first occurence of NAICS_CODE in our input files. For sure at this stage i would ask data scientists to precise
what exactly is being wanted to be analyzed by them. So on my own i decided to give to an output only this occupation which occurs
most times in our data, saving other occupations in form of number_certified_applications of course, didn't want to 
lose them. To be honest i have also spent some time trying to figure out how to sort with core python the data prioritizing
the number_certified_applications descending and then string - occupation ascending, however lambda helped me here very well.
<br/><br/>
Starting this task i thought that i will be able to create one function to handle top 10 occupations and top 10 states.
Nonetheless following the rules of task i found it hard to make dependency between desired layout of state_id e.g. FL, GA with 
worksite_postal_code. That is why i decided to get kinda official Zip Codes Database in csv from: https://simplemaps.com/data/us-zips site.
It helped me a lot to somehow connect worksite_postal_code to specific state_id and it was mainly reason that i was not able
to create one function to get top 10 occupation, top 10 states and things which would like analyze in the future...
