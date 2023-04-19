from bs4 import BeautifulSoup
# Read the contents of the HTML file
with open('index.html', 'r') as file:
  html = file.read()
number_of_ids = 0
# Parse the HTML code with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
def first_half(tag_name, attrs, level, text, no_of_children):
  global number_of_ids
  # Create a string representation of the attributes object
  attrs_str = ", ".join([f'{key}: "{value}"' if key != 'class' else f'className: "{value[0]}"' for key, value in attrs.items()])
  attrs_str = ''
  next_level = level + 1
  next_next_level = next_level + 1
  key_index = 0
  attrs_str += '\n' + '  '*next_next_level + 'key: "' + tag_name + '_' + str(number_of_ids) +'",'
  number_of_ids += 1
  for key, value in attrs.items():
    attrs_str += '\n'
    if(key == 'class'):
      attrs_str += '  '*next_next_level + 'className:"'
      for i in range(len(value)):
        if(i == 0):
          attrs_str += value[i]
        else:
          attrs_str += ' ' + value[i]
      attrs_str += '"'
    elif(key == 'aria-current'):
      attrs_str += '  '*next_next_level + '\'aria-current\':"'
      for i in range(len(value)):
        if(i == 0):
          attrs_str += value[i]
        else:
          attrs_str += value[i]
      attrs_str += '"'      
    else:
      attrs_str += '  '*next_next_level + key + ': '
      for i in range(len(value)):
        if(i == 0):
          attrs_str += '"' + value[i]
        elif(i == len(value)-1):
          attrs_str += value[i] + '"'
        else:
          attrs_str += value[i]
      if(len(value) == 1):
        attrs_str += '"'
    attrs_str += ','
    key_index += 1
  # Construct the final React component string
  component_str = '\n' + '  '*level + 'React.createElement(\n'
  next_level = level + 1
  next_next_level = next_level + 1
  component_str += '  '*next_level + '"' + tag_name + '",'
  component_str += '\n'
  component_str += '  '*next_level + "{"
  component_str += '  '*next_next_level + attrs_str
  component_str += '\n'
  component_str += '  '*next_level + "},"
  component_str += '\n'
  if(tag_name == 'img' or tag_name == 'input'):
    component_str = component_str
  else:
    component_str += '  '*next_level + '['
    if(no_of_children == 1 and text):
      component_str += '\n'
      component_str += '  '*next_next_level + '"' + text + '"'

  return component_str
def second_half(tag_name, attrs, level):
  next_level = level + 1
  component_str = '\n'
  if(tag_name == 'img' or tag_name == 'input'):
    component_str += '  '*next_level + "),"
  else:
    component_str += '  '*next_level + "]),"
  return component_str
# Recursive function to traverse and print tree graph of elements
def generate_react_component(element, level=0, result = ''):
  result = first_half(element.name, element.attrs, level, element.text, len(list(element.children)))
  # Recursively traverse and print child elements
  for child in element.children:
    if child.name is not None:
      result += generate_react_component(child, level+1, result)
  result += second_half(element.name, element.attrs, level)
  return result
output_js = generate_react_component(soup)
# Write the final React component code to a file
with open('output.js', 'w') as file:
  file.write(output_js)