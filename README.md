# Space Quiz

A desktop quiz application about space built with Python and Pygame.

## Requirements

- Python 3.x
- pygame

```bash
pip install pygame
mkdir images
type nul > questions.txt   # Windows
touch questions.txt        # Linux / macOS
```

## Running

```bash
python script.py
```

## Project Structure

```
├── script.py
├── questions.py
├── questions.txt
└── images/
```

## Question Format

Questions are loaded from `questions.txt`. Each line is one question:

```
Question text:Answer1,Answer2,Answer3!,Answer4
Question with image?,image.jpg:Answer1!,Answer2,Answer3,Answer4
```

- Separate question and answers with `:`
- Separate answers with `,`
- Mark the correct answer with `!` at the end
- Each question must have exactly **4 answers** and **1 correct answer**
- To attach an image to a question, add the filename after a `,` in the question part
- Place all images in the `images/` folder

### Example `questions.txt`

```
How many planets are in the Solar System?:6,7,8!,9
Which planet is shown?,images/saturn.jpg:Jupiter,Saturn!,Mars,Neptune
```