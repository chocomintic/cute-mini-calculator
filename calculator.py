import math
import re
import tkinter as tk
from math import cos, sin, tan, sqrt, log, exp

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Enhanced Calculator")
        master.configure(bg="#DAEAF6")

        # Create the entry field
        self.entry = tk.Entry(master, width=30, justify='right', font=('Helvetica', 16))
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
        
        # Create number buttons
        self.create_button("1", 1, 0)
        self.create_button("2", 1, 1)
        self.create_button("3", 1, 2)
        self.create_button("4", 2, 0)
        self.create_button("5", 2, 1)
        self.create_button("6", 2, 2)
        self.create_button("7", 3, 0)
        self.create_button("8", 3, 1)
        self.create_button("9", 3, 2)
        self.create_button("0", 4, 1)
        self.create_button(".", 4, 2)

        # Create operator buttons
        self.create_button("+", 1, 3)
        self.create_button("-", 2, 3)
        self.create_button("*", 3, 3)
        self.create_button("/", 4, 3)
        self.create_button("^", 5, 3)

        # Create function buttons
        self.create_button_span("=", 6, 3, 2, 1)
        self.create_button("C", 6, 0)
        self.create_button("CE", 6, 1)
        self.create_button("(", 5, 0)
        self.create_button(")", 5, 1)
        
        # Add scientific function buttons
        self.create_button("sin", 1, 4)
        self.create_button("cos", 2, 4)
        self.create_button("tan", 3, 4)
        self.create_button("sqrt", 6, 2)
        self.create_button("log", 4, 4)
        self.create_button("exp", 5, 4)
        self.create_button("pi", 5, 2)
        self.create_button("e", 4, 0)

    def create_button(self, text, row, column):
        if text.isdigit() or text == '.' or text == 'e':
            # Number buttons - light gray
            bg_color = '#CBCEEE'
            fg_color = 'black'
        elif text in ['+', '-', '*', '/', '^']:
            # Operator buttons - orange
            bg_color = '#E8DAF0'
            fg_color = 'black'
        elif text in ['C', 'CE']:
            # Clear buttons - red
            bg_color = '#F3E4F5'
            fg_color = 'black'
        elif text in ['sin', 'cos', 'tan', 'sqrt', 'log', 'exp', 'pi']:
            # Scientific buttons - blue
            bg_color = '#FCDCE1'
            fg_color = 'black'
        else:
            # Other buttons - dark gray
            bg_color = '#D8BEE5'
            fg_color = 'black'
            
        button = tk.Button(self.master, text=text, width=5, height=2, 
                          font=('Helvetica', 12, 'bold'), 
                          bg=bg_color, fg=fg_color,
                          activebackground='#34495E', activeforeground='white',
                          command=lambda: self.button_click(text))
        button.grid(row=row, column=column, padx=5, pady=5)

    def create_button_span(self, text, row, column, columnspan, rowspan):
        """Create a button that spans multiple columns"""
        button = tk.Button(self.master, text=text, height=2, 
                          font=('Helvetica', 12, 'bold'),
                          bg='#DBCDF0', fg='black', 
                          activebackground='#DBCDF0', activeforeground='black',
                          command=lambda: self.button_click(text))
        button.grid(row=row, column=column, columnspan=columnspan, rowspan = rowspan, padx=5, pady=5, sticky='ew')
    
    def button_click(self, text):
        if text == "=":
            try:
                expression = self.entry.get()
                # Clean up the input - add parentheses for trig functions if missing
                cleaned = re.sub(r'(sin|cos|tan|sqrt|log|exp)(\d+\.?\d*)', r'\1(\2)', expression)
                result = self.evaluate_expression(cleaned)
                
                if isinstance(result, str) and result.startswith("Error"):
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, result)
                else:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, str(result))
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, f"Error: {str(e)}")
        elif text == "C":
            self.entry.delete(0, tk.END)
        elif text == "CE":
            self.entry.delete(len(self.entry.get())-1, tk.END)
        elif text in ["sin", "cos", "tan", "sqrt", "log", "exp"]:
            # Insert function with opening parenthesis
            self.entry.insert(tk.END, text + "(")
        elif text in ["pi", "e"]:
            # Insert constants
            self.entry.insert(tk.END, text)
        else:
            self.entry.insert(tk.END, text)

    def evaluate_expression(self, expression):
        """
        Safely evaluate mathematical expressions including trigonometric functions
        """
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        
        # Define safe functions for evaluation
        safe_dict = {
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'sqrt': sqrt,
            'log': log,
            'exp': exp,
            'pi': math.pi,
            'e': math.e,
            '__builtins__': None
        }
        
        try:
            # Evaluate the expression safely
            result = eval(expression, safe_dict)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

# Create and run the calculator
root = tk.Tk()
calculator = Calculator(root)
root.mainloop()