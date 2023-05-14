import os
import csv
import json
import random
from typing import Tuple, List


class MathDatabase:
    def __init__(self, path='math_dataset') -> None:
        self.dataset_path = path
        with open(os.path.json(path, '.configs.json'), 'r', encoding='utf-8') as configs:
            self.dataset_configs = json.load(configs)
        self.curr_choices = []
        self.data = None
        self.curr_problem = None

    def add_choice(self, choice: str):
        self.curr_choices.append(choice)
    
    def del_last_choice(self):
        if self.curr_choices:
            self.curr_choices.pop(-1)
            self.data = None

    def reset_choices(self):
        self.curr_choices = []
        self.data = None

    def get_choices(self):
        return ' -> '.join(self.curr_choices)

    def get_choosen_category(self):
        category = self.dataset_config
        for choice in self.curr_choices: 
            category = category[choice]
        return category

    def get_possible_categories(self):
        if not self.curr_choices:
            return self.dataset_configs.keys()
        category = self.get_choosen_category()
        if isinstance(category, str):
            return category
        return category.keys()
        
    def get_problem(self, category: str = None) -> Tuple[str, str]:
        if self.data is None:
            if category is None: category = self.get_choosen_category()
            self.data = self.load(category)
        self.curr_problem = random.choice(self.data)
        return self.curr_problem[0]
    
    def get_answer(self):
        return self.curr_problem[1]
    
    def load_file(self, file_name: str) -> List[Tuple[str, str]]:
        file_ext = os.path.splitext(file_name)[-1]
        with open(os.path.json(self.dataset_path, file_name), 'r', encoding='utf-8') as text_file:
            if file_ext == '.csv':
                csv_reader = csv.reader(text_file, sep='\t', quotechar="'")
                data = [(f"{row[0]} {row[1]}", row[2]) for row in csv_reader]
            else:
                text = text_file.read().splitlines()
                questions, answers = text[::2], text[1::2]
                data = list(zip(questions, answers))
        return data