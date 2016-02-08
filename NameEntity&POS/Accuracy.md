PART IV

1.What is the accuracy of your part-of-speech tagger?

Answer: The lowest error rate is about 0.0564, so the best accuracy of my part-of-speech tagger is about 94.36%.
Generally speaking, the accuracy is about 94% ~ 95%.

2.What are the precision, recall and F-score for each of the named entity types for your
named entity recognizer, and what is the overall F-score?

Answer: The performance measures of each of the named entity types are as follows.

BLOC entity precision is: 0.6501901140684411;

BLOC entity recall is: 0.5213414634146342;

BLOC entity F-score is: 0.5786802030456852;

BPER entity precision is: 0.7964601769911505;

BPER entity recall is: 0.36824877250409166;

BPER entity F-score is: 0.5036373810856184;

BORG entity precision is: 0.6900858704137393;

BORG entity recall is: 0.5209192692987625;

BORG entity F-score is: 0.5936870382807253;

BMISC entity precision is: 0.44107744107744107;

BMISC entity recall is: 0.2943820224719101;

BMISC entity F-score is: 0.353099730458221;

And the overall F-score of my named entity recognizer is as follows.

Overall precision is: 0.67462482946794;

Overall recall is: 0.4549218031278749;

Overall F-score is: 0.5434065934065935;

3.What happens if you use your Naive Bayes classifier instead of your perceptron classifier
(report performance metrics)? Why do you think that is?

Answer: If using Naive Bayes classifier

(1) The error rate is 0.08417877707704963, so the accuracy of part-of-speech task is about 91.59%.

(2) The performance measure of named entity recognizing task are as follows.

BLOC entity precision is: 0.19325842696629214;

BLOC entity recall is: 0.6117886178861789;

BLOC entity F-score is: 0.29373017809221763;

BPER entity precision is: 0.26063470627954083;

BPER entity recall is: 0.3158756137479542;

BPER entity F-score is: 0.28560858305586384;

BORG entity precision is: 0.13604894541941717;

BORG entity recall is: 0.4979375368296995;

BORG entity F-score is: 0.21370763783510371;

BMISC entity precision is: 0.08650519031141868;

BMISC entity recall is: 0.056179775280898875;

BMISC entity F-score is: 0.06811989100817438;

Overall precision is: 0.1674477289113194;

Overall recall is: 0.4273229070837167;

Overall F-score is: 0.24061124061124062;

(3) From the above we can see that if using Naive Bayes classifier instead of using 
perceptron classifier, both the accuracy of part-of-speech task and performance measure
of named entity recognizing task are become lower. I think this is because the Naive
Bayes classifier does not consider the dependency among the features in each feature
vector when it classifying. 



Python command usage for csci544 hw2

For part I:

(1)usage: perceplearn.py [-h devfile] [-i iter_wanted] input_path model_path

   positional arguments:
   
     input_path  path of legal formatted file as input
     
     model_path  path of model file as output
  
   optional arguments:
   
     -h  path of development data file
     
     -i  number of iteration for update the weights
     
(2)usage: percepclassify.py [-h] model_path

   positional arguments:
   
     model_path  path of model file

   optional arguments:
   
     -h, --help  show this help message and exit

For part II:

(1)usage: postrain.py [-h devfile] [-i iter_wanted] input_path model_path

   positional arguments:
   
     input_path  path of legal formatted file as input
     
     model_path  path of model file as output
  
   optional arguments:
   
     -h  path of development data file
     
     -i  number of iteration for update the weights
  
(2)usage: postag.py [-h] model_path

   positional arguments:
   
     model_path  path of model file
  
   optional arguments:
   
     -h, --help  show this help message and exit

For part III:

(1)usage: nelearn.py [-h devfile] [-i iter_wanted] input_path model_path

   positional arguments:
   
     input_path  path of legal formatted file as input
     
     model_path  path of model file as output
  
   optional arguments:
   
     -h  path of development data file
     
     -i  number of iteration for update the weights
  
(2)usage: netag.py [-h] model_path

   positional arguments:
   
     model_path  path of model file

   optional arguments:
   
     -h, --help  show this help message and exit