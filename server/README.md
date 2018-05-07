Research part of the Bot building. Some techniques are considered, some experiments are conducted.

- `exploring_chatbot.ipynb`

Files which comprise the running server

- `server.py` - all-the-host-port-etc-server-stuff


- `chatbot.py` - ChatBot
- `dialogue_manager.py` - kind of medium between the server and Chatbot: gets a question, preprocesses it, sends to ChatBot, receives the answer and returns it
- `utils.py` - some auxiliary functions

Scripts for downloading, reading and preprocessing data for the chatbot's training

- `download_cornell.sh` - downloads Cornell movie dialogues dataset (small size)
- `download_opensubs.sh` - downloads Opensubs movie subtitles dataset (large size)
- `datasets.py` - module to be imported in the scripts, that exports functions for reading datasets
- `example.py` - example of reading the datasets

File containing the command by which StarSpace model was trained (some details about StarSpace model are in `exploring_chatbot.ipynb`)

* `starspace_train_command.txt`