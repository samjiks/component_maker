# Component Adder Test

## Requirements
Python 3.3 and above

## Run
python app.py -r

## How it Works 
We understand the working from the Generated logs
- Components with workers which we could see what is added to the list
   [{'w2': ['P'], 'w1': ['B']}, {'w3': [], 'w4': []}, {'w6': [], 'w5': []}]
- Creating Component A on to the conveyer belt at 19 to see what is being 
  added to the converyer belt
- Components which are currently on the conveyer belt ['B', '', '', 'P', '', '', 'B', 'B', '', 'A', 'A', 'B'] 


## TO DO
- Terminate the process if all and only 'P' or empty slots or don't have
  the matching components on the converyer belt to 
  fulfill the production cycle
- Create a single JSON entry of all the objects onto a .txt file 
  required to create a simulation ASCII on the the command line
