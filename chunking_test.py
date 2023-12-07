import re


def chunk_output(text: str):
    # Define the regex pattern to match text between triple backticks, including the backticks
    pattern = r'(```.*?```)'
    
    # Split the text based on the pattern, retain the delimiters
    parts = re.split(pattern, text)

    # Return the non-empty parts
    return [part for part in parts if part]

text = r"""Certainly! Below is an example of a 10 route Flask API with math functions. Please note that this is a conceptual example and is not intended to be run as-is. For each route, I'll provide the function and an example of how it might be used.

First, let's make sure Flask is installed:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Route 1: Add two numbers
@app.route('/add', methods=['GET'])
def add():
    n1 = float(request.args.get('n1', 0))
    n2 = float(request.args.get('n2', 0))
    result = n1 + n2
    return jsonify({'result': result})

# Route 2: Subtract two numbers
@app.route('/subtract', methods=['GET'])
def subtract():
    n1 = float(request.args.get('n1', 0))
    n2 = float(request.args.get('n2', 0))
    result = n1 - n2
    return jsonify({'result': result})

# Route 3: Multiply two numbers
@app.route('/multiply', methods=['GET'])
def multiply():
    n1 = float(request.args.get('n1', 1))
    n2 = float(request.args.get('n2', 1))
    result = n1 * n2
    return jsonify({'result': result})

# Route 4: Divide two numbers
@app.route('/divide', methods=['GET'])
def divide():
    n1 = float(request.args.get('n1', 1))
    n2 = float(request.args.get('n2', 1))
    if n2 == 0:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    result = n1 / n2
    return jsonify({'result': result})

# Route 5: Modulus two numbers
@app.route('/modulus', methods=['GET'])
def modulus():
    n1 = int(request.args.get('n1', 0))
    n2 = int(request.args.get('n2', 1))
    if n2 == 0:
        return jsonify({'error': 'Cannot take modulus by zero'}), 400
    result = n1 % n2
    return jsonify({'result': result})

# Route 6: Raise to power
@app.route('/power', methods=['GET'])
def power():
    base = float(request.args.get('base', 1))
    exponent = float(request.args.get('exponent', 1))
    result = base ** exponent
    return jsonify({'result': result})

# Route 7: Square root
@app.route('/sqrt', methods=['GET'])
def sqrt():
    number = float(request.args.get('number', 0))
    if number < 0:
        return jsonify({'error': 'Cannot take the square root of a negative number'}), 400
    result = number ** 0.5
    return jsonify({'result': result})

# Route 8: Logarithm base 10
@app.route('/log', methods=['GET'])
def l

og():
    number = float(request.args.get('number', 1))
    if number <= 0:
        return jsonify({'error': 'Logarithm is not defined for non-positive numbers'}), 400
    import math
    result = math.log10(number)
    return jsonify({'result': result})

# Route 9: Natural logarithm
@app.route('/ln', methods=['GET'])
def ln():
    number = float(request.args.get('number', 1))
    if number <= 0:
        return jsonify({'error': 'Natural logarithm is not defined for non-positive numbers'}), 400
    import math
    result = math.log(number)
    return jsonify({'result': result})

# Route 10: Factorial
@app.route('/factorial', methods=['GET'])
def factorial():
    number = int(request.args.get('number', 0))
    if number < 0:
        return jsonify({'error': 'Factorial is not defined for negative numbers'}), 400
    import math
    result = math.factorial(number)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
```
Now let's see examples of how these routes might be used:

1. Addition: `http://localhost:5000/add?n1=10&n2=5` should return `{"result": 15.0}`
2. Subtraction: `http://localhost:5000/subtract?n1=10&n2=5` should return `{"result": 5.0}`
3. Multiplication: `http://localhost:5000/multiply?n1=10&n2=5` should return `{"result": 50.0}`
4. Division: `http://localhost:5000/divide?n1=10&n2=5` should return `{"result": 2.0}`
5. Modulus: `http://localhost:5000/modulus?n1=10&n2=3` should return `{"result": 1}`
6. Power: `http://localhost:5000/power?base=2&exponent=3` should return `{"result": 8.0}`
7. Square Root: `http://localhost:5000/sqrt?number=16` should return `{"result": 4.0}`
8. Logarithm base 10: `http://localhost:5000/log?number=100` should return `{"result": 2.0}`
9. Natural Logarithm: `http://localhost:5000/ln?number=7.38905609893` should return approximately `{"result": 2.0}`
10. Factorial: `http://localhost:5000/factorial?number=5` should return `{"result": 120}`

Remember that you need to have Flask running the development server for these examples to work. Use the `app.run()` method to start it, and these endpoints will become accessible via the URLs provided above, assuming that the server is running on `localhost` and listening to port `5000`."""

chunks = chunk_output(text)


for chunk in chunks:
    print(chunk)
    print("-----")
print("Lenght of chunks: " + str(len(chunks)))

