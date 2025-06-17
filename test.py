print("Hello, World!")

def calculator():
    print("Simple Calculator")
    print("Operations: + (add), - (subtract), * (multiply), / (divide)")
    print("Type 'clear' to reset, 'exit' to quit\n")

    result = None
    
    while True:
        # Get user input
        user_input = input("Enter operation: ").strip().lower()
        
        # Exit condition
        if user_input in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        # Clear/reset condition
        if user_input == 'clear':
            result = None
            print("Calculator reset\n")
            continue
        
        # Validate and parse input
        parts = user_input.split()
        if len(parts) < 2:
            print("Invalid input! Please enter at least two values\n")
            continue
        
        # Parse numbers and operator
        try:
            # Handle continuation from previous result
            if result is not None:
                num1 = result
                operator = parts[0]
                num2 = float(parts[1])
            else:
                num1 = float(parts[0])
                operator = parts[1]
                num2 = float(parts[2])
        except (ValueError, IndexError):
            print("Invalid input format! Use: [number] [operator] [number]\n")
            continue
        
        # Perform calculation
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("Error: Division by zero!\n")
                continue
            result = num1 / num2
        else:
            print(f"Invalid operator: '{operator}'. Valid operators: +, -, *, /\n")
            continue
        
        # Display result
        print(f"Result: {result}\n")

# Start the calculator
if __name__ == "__main__":
    calculator()
