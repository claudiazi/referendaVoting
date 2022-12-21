# referendaVoting

This repo is to build a dash dashboard to analyse the performance of Kusama referenda voting system.

### Summary of dashboard
The dashboard has three tabs:
- **Main dashboard:**
  
  Present the most important statics of ongoing and all referenda to show some insightful trends. 
  You can filter out a specific group of referenda based on referendum_index, section, method and proposer.
  
- **Single referendum view:**
  
  If you are interested in the performance of a specific referendum, you can find relevant information in this tab.
  
- **Single account view:**

  If you are interested in the voting history of a specific address, this is the playground you need.


### Running the app locally:
1. Set up virtual environment

```
python -m venv venv
source venv/bin/activate  # Windows: \venv\scripts\activate
pip install -r requirements.txt
```

2. Run script
```
python index.py
```
