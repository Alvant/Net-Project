# Net Project: Dialog Bot

---



This is the final work on [Network Technologies](http://acm.mipt.ru/twiki/bin/view/Networks), a course by [Dmitry Podlesnykh](http://wikimipt.org/wiki/%D0%9F%D0%BE%D0%B4%D0%BB%D0%B5%D1%81%D0%BD%D1%8B%D1%85_%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B9_%D0%90%D1%80%D1%82%D1%83%D1%80%D0%BE%D0%B2%D0%B8%D1%87) at [Moscow Institute of Physics and Technology (MIPT)](https://mipt.ru/english/).



[A chatbot](https://github.com/Alvant/Net-Project/blob/master/server/chatbot.py) is running on the Amazon server... And one can have a talk with it!



## Project Structure



There are two folders: *client* and *server*.



In *client* folder there are [python client](https://github.com/Alvant/Net-Project/blob/master/client/client.py) and [C# client](https://github.com/Alvant/Net-Project/blob/master/client/client.cs) with corresponding [exe file](https://github.com/Alvant/Net-Project/blob/master/client/client.exe).



*Server* folder contains

* [Python server](https://github.com/Alvant/Net-Project/blob/master/server/server.py)
* [Chatbot](https://github.com/Alvant/Net-Project/blob/master/server/chatbot.py)
* And numerous files connected with Chatbot's training and functioning. Eager readers can find all the details about Chatbot in the [jupyter notebook](https://github.com/Alvant/Net-Project/blob/master/server/exploring_chatbot.ipynb)





## Requirements



There are two ways to chat with the bot

* Download [binary client](https://github.com/Alvant/Net-Project/blob/master/client/client.exe) and run it
* Download [python client](https://github.com/Alvant/Net-Project/blob/master/client/client.py). In order to make it work, one should also have Python 3 with [socket module](https://docs.python.org/3/library/socket.html) installed on the PC


If you managed to complete either step from above, I assume that you also have Internet connection. It is also important :)




## Usage



Just type something, some sentence or phrase, and press Enter.

Not long after that you will see the Chatbot's answer. If it is still running on the server :)



If you want to finish the dialog, type *Ciao!* or *ciao!* (or, actually, any other upper-lower case *ciao* combination with one exclamation mark *!* after).



## Acknowledgements & Advertisements



The work in general is, in fact, a mixture of several homeworks on two courses from [Coursera platform](https://www.coursera.org/)

* [NLP course by Higher School of Economics](https://www.coursera.org/learn/language-processing) (and I want to single out the chatbot-assignment from the final week)
* [Python course by MIPT (in Russian)](https://www.coursera.org/learn/programming-in-python) (special thanks for the topic *Multi-threaded and asynchronous programming* covered in the final week)