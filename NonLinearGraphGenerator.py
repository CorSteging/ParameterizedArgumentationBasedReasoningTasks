import pandas as pd
import random

PREAMBLE = "The following is a reasoning puzzle. Witnesses should be believed unless there is testimony that they are lying. Now consider the following facts:"

QUESTION_PREAMBLE = "Question: should it be believed that "
QUESTION_ADDITIONAL = "End your answer with: \"Answer: yes or no\""

DEFAULT_NAMES = 'ontologies/names.csv'
DEFAULT_STATEMENTS = 'ontologies/statements.csv'

class Case:
    def __init__(self, num_arguments, format, prompt, answer):
        self.num_arguments = num_arguments
        self.format = format
        self.prompt = prompt
        self.answer = answer

    def __repr__(self):
        return "Case with " + str(self.num_arguments) + " arguments and the following prompt:\n###\n" + str(self.prompt) +"\n###\n\nAnswer: " + str(bool(self.answer))
        
class CaseGenerator:
    def __init__(self, default_names=DEFAULT_NAMES, default_statements=DEFAULT_STATEMENTS, shuffle_arguments=False):
        self.names = pd.DataFrame.from_dict({'name': pd.read_csv(default_names)['name'].unique()})
        self.statements = pd.read_csv(default_statements)
        self.shuffle_arguments = shuffle_arguments

    def generate_intial_sentence(self, name_list):
        #Generate a new name
        name = random.choice(name_list)

        #Generate a statement
        df = self.statements.sample(n=1)
        statement = df['statement'].iloc[0]
        statement_q = df['statement_q'].iloc[0]
 
        #Create a prompt from the statement
        prompt = "Witness " + name + " says that " + statement + "."
        return name, prompt, statement, statement_q

    def generate_sentence(self, cur_argument, previous_name, name_list):
        #Generate a new name
        name = random.choice(name_list)

        #Generate a prompt
        prompt = "Witness " + name + " says that witness " + previous_name + " is lying."
        return name, prompt

    def partitions(self, n, I=1):
        '''
        Yields a generator that generates all partitions for integer n
        '''
        yield (n,)
        for i in range(I, n//2 + 1):
            for p in self.partitions(n-i, i):
                yield (i,) + p
                
    def generate_case(self, format):
        # if linear and num_args is provided
        if isinstance(format, int): format = [format-1] 
        num_arguments = sum(format) + 1
        name_list = list(self.names['name'])
        all_arguments = []
        if num_arguments > len(self.names['name']):
            print('ERROR: More arguments than names in the ontology')
            return None
        
        prompt = PREAMBLE + '\n'

        # Create the main argument
        first_name, sentence, statement, statement_q = self.generate_intial_sentence(name_list)
        name = first_name
        all_arguments.append(sentence)
        name_list.remove(name)
        
        # Create all of the arguments that attack main argument
        for chain in format:
            for x in range(0, chain):
                name, sentence = self.generate_sentence(x, name, name_list)
                all_arguments.append(sentence)
                name_list.remove(name)
            name = first_name


        if self.shuffle_arguments: random.shuffle(all_arguments)
        prompt += '\n'.join(all_arguments)
        prompt += '\n' + QUESTION_PREAMBLE + statement_q +"\n" + QUESTION_ADDITIONAL

        answer = 1#num_arguments%2
        if any(n%2 for n in format): answer = 0
        
        return Case(num_arguments, format, prompt, answer)


    def generate_all_cases(self, max_args):
        parts = list(self.partitions(max_args-1))
        all_cases = []
        for part in parts:
            all_cases.append(self.generate_case(part))
                    
        return all_cases
