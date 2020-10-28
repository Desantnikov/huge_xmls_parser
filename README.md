# huge_xmls_parser

Job was to parse, concatenate, filter and aggregate a sequence of ~9GB xml files. Then data should be divided by regions and saved 
to corresponding excel files, max 100k of rows in each. 

Code is not refactored and looks not very pretty since it was a one-time job that is already done. 
But still can help someone to see example of handling huge xml files. 

## Main concepts that I used: 

reading xml in parts

using __slots__ 

optimizing dataframe's columns types
    
Before using them even 16GB of RAM and 50GB of swap was not enough to process this data due to OutOfMemoryException.  
After using them 16GB of RAM and 15GB of swap was enough to process all data. 
    
    
