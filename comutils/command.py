
import os
from cominfer.command_inferrer import CommandInferrer

def main():
    description = 'Command line tool description'
    directory = os.path.dirname(os.path.realpath(__file__))
    CommandInferrer(description, directory).infer()
