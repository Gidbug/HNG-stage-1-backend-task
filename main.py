from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    return sum(int(digit) ** len(str(n)) for digit in str(n)) == n

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get('number')
    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400

    num = int(num)
    properties = []
    if is_prime(num): properties.append("prime")
    if is_perfect(num): properties.append("perfect")
    if is_armstrong(num): properties.append("armstrong")
    properties.append("even" if num % 2 == 0 else "odd")

    fun_fact = requests.get(f"http://numbersapi.com/{num}").text

    return jsonify({
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(digit) for digit in str(num)),
        "fun_fact": fun_fact
    })

if __name__ == '__main__':
    app.run(debug=True)
