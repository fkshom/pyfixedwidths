pyfixedwidths
------------------------

>>> pip install pyfixedwidths

>>> from pyfixedwidths import FixedWidthFormatter
>>> text = (
>>> "1,2,3,4\n"
>>> "11,,33,44\n"
>>> )
>>> 
>>> listofdict = [
>>>     dict(name="John Doe", age=20, hobby="swim"),
>>>     dict(name="John Smith", age=100, job="teacher"),
>>> ]
>>> 
>>> array = [
>>>     [1, None, 3, 4],
>>>     [11, 22, None, 44],
>>> ]
>>> 

>>> fw = FixedWidthFormatter()
>>> fw.from_text(text).to_text(padding=1)
>>> #=>
>>>     ("1  , 2 , 3  , 4 \n"   
>>>      "11 ,   , 33 , 44\n")
>>> 
>>> fw.from_text(text).to_array(padding=1)
>>> #=>
>>>     [["1  "," 2 "," 3  "," 4 "],
>>>      ["11 ","   "," 33 "," 44"],]
>>> 

>>> fw = FixedWidthFormatter()
>>> fw.from_array(array).to_text(padding=0)
>>> #=>
>>>     ("1 ,None,3   ,4 \n"
>>>      "11,    ,None,44\n")
>>> 
>>> fw.from_array(array).to_array(padding=0)
>>> #=>
>>>     [["1 ","None","3   ","4 "],
>>>      ["11","    ","None","44"],]
>>> 

>>> fw = FixedWidthFormatter(schema=schema)
>>> fw.from_dict(listofdict).to_list(padding=0)
>>> #=>
>>>     ("name      ,age,hobby,job    \n"
>>>      "John Doe  ,20 ,swim ,       \n"
>>>      "John Smith,100,     ,teacher\n")
>>> 
>>> fw.from_dict(listofdict).to_list(padding=0)
>>> #=>
>>>     [["name      ", "age", "hobby", "job    "],
>>>      ["John Doe  ", "20 ", "swim ", "       "],
>>>      ["John Smith", "100", "     ", "teacher"],]

>>> schema = [
>>>     dict(
>>>         justification="rjust"
>>>     ),
>>>     dict(
>>>         format=":>5s"
>>>     ),
>>>     dict(),
>>>     dict(
>>>         format=":2s"
>>>     )
>>> ]
>>> 
>>> fw = FixedWidthFormatter(schema=schema)
>>> fw.from_dict(listofdict).to_text(padding=2)
>>> #=>
>>>     ("      name  ,    age  ,  hobby  ,  job\n"
>>>      "  John Doe  ,     20  ,  swim   ,    \n"
>>>      "John Smith  ,    100  ,         ,  teacher\n")
>>> 
>>> fw.from_dict(listofdict, headers=["hobby", "job", "location", "name"]).to_text(padding=1)
>>> #=>
>>>     (   "hobby ,     job , location , name\n"
>>>         " swim ,         ,          , John Doe\n"
>>>         "      , teacher ,          , John Smith\n")
