# TagIt

TagIt is a simple image labeling tool built in Python that allows users to assign labels to images using keyboard shortcuts. This tool is particularly useful for grouping images for classification tasks.



## Features
* Display images from a specified folder for labeling
* Assign labels to images using keyboard shortcuts
* Save labeled images and their corresponding labels in a CSV file
* Option to assign multiple labels to each image
* Lightweight and easy to use

## Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/Mohammad-Mahdi-Hosseini/TagIt.git
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```



## Usage
Here is an example of how to use the TagIt module:

```python
from TagIt import TagIt

Images_dir = '/path/to/images'
BackUp_dir = '/path/to/backup/folder'
classes_input = {'1': 'class1', '2': 'class2', '3': 'class3'}
tagger = TagIt(Images_dir, BackUp_dir, classes_input)
```
This will create an instance of the TagIt class, which will display the first image in the Images_dir folder. You can then use the 1, 2, and 3 keys to label the image with the corresponding classes, and the label information will be saved in a CSV file in the Images_dir folder.

## Contributing
If you encounter any issues or have suggestions for new features, feel free to open an issue or submit a pull request on the GitHub repository. All contributions are welcome!

## License
This module is released under the MIT License.
