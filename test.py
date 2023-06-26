import prompt_toolkit
from prompt_toolkit import prompt, print_formatted_text

text = prompt('Give me some input: ')
print('You said: %s' % text)

print_formatted_text('Hello world')