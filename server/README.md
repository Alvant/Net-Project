Research part of the Bot building. Some techniques are considered, some experiments are conducted.

- `exploring_chatbot.ipynb`

Files which comprise the running server

- `server.py` – all-the-host-port-etc-server-stuff


- `chatbot.py` – ChatBot
- `dialogue_manager.py` – kind of medium between the server and Chatbot: gets a question, preprocesses it, sends to ChatBot, receives the answer and returns it
- `datasets.py` – module to be imported in the scripts, that exports functions for reading datasets
- `utils.py` – some auxiliary functions
- `white_list.txt` – allowed clients' ip addresses (however, the address verification procedure on server is now disabled; creating the config file and making white list were the additional tasks when taking exam in the [course](http://acm.mipt.ru/twiki/bin/view/Networks))

Folder [download_datasets](https://github.com/Alvant/Net-Project/tree/master/server/download_datasets) contains scripts for downloading and preprocessing data for the chatbot's training

- `download_cornell.sh` – downloads Cornell movie dialogues dataset (small size)
- `download_opensubs.sh` – downloads Opensubs movie subtitles dataset (large size)
- `example.py` – example of reading the datasets

In folder [misc](https://github.com/Alvant/Net-Project/tree/master/server/misc) there is a file with command by which the StarSpace model was trained (some details about StarSpace model are in `exploring_chatbot.ipynb`)

* `starspace_train_command.txt`