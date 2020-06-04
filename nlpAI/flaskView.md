# Email AI Classifier - Flask View Interface

Specifies the RESTfull hmtl PUT/GET/POST interface between the html/javascript client frontend view and the python Flask backend running on a google appengine.

The email database class has a cursor that is initialized to point to the first email. Some of the calls desctipbed here will move that cursor.

All the functions are javascript jquery calls. All arguments and returns are ascii strings

#TrainConf - Get confidence calculation for training set size and error margin
Called to calculate a new AI confidence when train goal or err margin changes to get new AI confidence percent
Args:
  * trainSz - 0-n; number of emails classified by a person
  * errMargin 0-100; acceptable +/- difference between trained true percent and AI true percent

Return:
  * trainConf - mm.nn; percent confidence that the AI algorithm is as good as the trainer  

javascript template:
  $.get("/getTrainConf",{trainSz:x,errMargin:y},
    function(data) {
      var trainConf = $.parseJSON(data);
      //..... your code here ...........
    }
  )
  .fail(function(e){
      //..... your code here ...........
  });

#RunAI - Get results of AI classifier 
Called to train selected AI algorithm and run it on all the emails
Args:
  * aiAlg - rfa,svn,nvb; one of three AI algorithms to use
  * errMargin 0-100; acceptable +/- difference between trained true percent and AI true percent

Return:
  * aiData{aiTrue:x,falsePos:y,falseNeg:z,aiOK:w}
    * aiTrue - 0-100; percent of emails that the AI algorithm classified as true
    * falsePos - 0-n; number of false trained emails that the AI algorithm classified true 
    * falseNeg - 0-n; number of true trained emails that the AI algorithm classified false 
    * aiOK - pass/fail; pass = AI true percent within error margin of person trained true percent

javascript template:
  $.get("/runAI",{errMargin:x,aiAlg:y},
    function(data) {
      var aiData = $.parseJSON(data);
      //..... your code here ...........
    }
  )
  .fail(function(e){
      //..... your code here ...........
  });


#GoTo - Get an Email by ID
Called to get an email by its ID and move the email database cursor to that email.
Args:
  * emailID - format = fileID_page_pagePosition

Return:
  * emailData{emailID:x,emailText:y,aiHypo:z,trainHypo:w}
    * emailID - format = fileID_page_pagePosition
    * email - complete email text
    * aiHypo - true/false/none; result of AI classifier
    * trainHypo - true/false/none; result of training

javascript template:
  $.get("/runAI",{emailID},
    function(data) {
      var emailData = $.parseJSON(data);
      //..... your code here ...........
    }
  )
  .fail(function(e){
      //..... your code here ...........
  });

#TrainEmail - Set the human hypothesis for currently displayed email

Args:
  * human hypo - true/false/none

Return:
  * trained size - 0-n
  * trained true - 0-100%

#GetNext - Get next email

Args:
  * mode - read/search/train

Return:
  * emailID - format = fileID_page_pagePosition
  * email - complete email text
  * AI hypo - true/false/none
  * human hypo - true/false/none

#GetPrev - Get previous email

Args:
  * mode - read/search/train

Return:
  * emailID - format = fileID_page_pagePosition
  * email - complete email text
  * AI hypo - true/false/none
  * human hypo - true/false/none

