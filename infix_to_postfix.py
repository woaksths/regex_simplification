#!/usr/bin/env python
# coding: utf-8


from FAdo.reex import *
import copy

class Conversion: 
    def __init__(self, capacity): 
        self.top = -1 
        self.capacity = capacity 
        self.array = [] 
        self.output = [] 
        self.precedence = {'+':1, '-':2, '*':3} 
      
    # check if the stack is empty 
    def isEmpty(self): 
        return True if self.top == -1 else False
      
    # Return the value of the top of the stack 
    def peek(self): 
        return self.array[-1] 
      
    # Pop the element from the stack 
    def pop(self): 
        if not self.isEmpty(): 
            self.top -= 1
            return self.array.pop() 
        else: 
            return "$"
      
    # Push the element to the stack 
    def push(self, op): 
        self.top += 1
        self.array.append(op)  
  
    # is operand  
    def isOperand(self, ch): 
        if ch == '1' or ch == '0':
            return True
        return False 
  
    # Check if the precedence of operator is strictly 
    # less than top of stack or not 
    def notGreater(self, i): 
        try: 
            a = self.precedence[i] 
            b = self.precedence[self.peek()] 
            return True if a  <= b else False
        except KeyError:  
            return False
              
    # The main function that converts given infix expression 
    # to postfix expression 
    def infixToPostfix(self, exp): 
        for idx,i in enumerate(exp): 
            # If the character is an operand,  
            # add it to output 
            if self.isOperand(i): 
                self.output.append(i) 
              
            # If the character is an '(', push it to stack 
            elif i  == '(': 
                self.push(i) 
  
            # If the scanned character is an ')', pop and  
            # output from the stack until and '(' is found 
            elif i == ')': 
                while( (not self.isEmpty()) and self.peek() != '('): 
                    a = self.pop()
                    self.output.append(a) 
                if (not self.isEmpty() and self.peek() != '('): 
                    return -1
                else: 
                    self.pop() 
            # An operator is encountered 
            else: 
                while(not self.isEmpty() and self.notGreater(i)): 
                    self.output.append(self.pop()) 
                self.push(i) 

        # pop all the operator from the stack 
        while not self.isEmpty(): 
            self.output.append(self.pop()) 
    
    def append_paren(self, ex, p):
        return '(' + ex[0] + ')' if ex[1] < p else ex[0]

    
    def reduce(self, rex):
        stk = []

        for x in rex:
            if x in '01':
                stk.append((x, 999999))
            elif x == '+':
                # priority 1
                h2 = stk.pop()
                h1 = stk.pop()

                h1 = self.append_paren(h1, 1)
                h2 = self.append_paren(h2, 1)
                stk.append((h1 + '+' + h2, 1))
            elif x == '-':
                # priority 2
                h2 = stk.pop()
                h1 = stk.pop()

                h1 = self.append_paren(h1, 2)
                h2 = self.append_paren(h2, 2)
                stk.append((h1 + '' + h2, 2))
            elif x == '*':
                # priority 3
                h1 = stk.pop()

                h1 = self.append_paren(h1, 3)        
                stk.append((h1 + '*', 3))

        assert(len(stk) == 1)
        return stk[0][0]
    
    
    def cal_postfix(self):
        stack = []
        output = copy.deepcopy(self.output)
        
        while len(output) > 0:
            element = output.pop(0)
            if element == '1' or element =='0':
                stack.append(element)
            elif element == '*':
                popped_element = stack.pop()
                stack.append('('+popped_element+')*')
            elif element == '-':
                popped_element1 = stack.pop()
                popped_element2 = stack.pop()
                stack.append('{}{}'.format(popped_element2,popped_element1))
            elif element == '+':
                popped_element1 = stack.pop()
                popped_element2 = stack.pop()
                stack.append('({}+{})'.format(popped_element2,popped_element1))
        assert(len(stack) ==1)
        return ''.join(stack)


def preprocessing_concat(regex):
    output = ''
    for idx in range(len(regex)):
        if idx  >= len(regex)-1:
            output += regex[idx]
            break

        char1 = regex[idx]
        char2 = regex[idx+1]
        
        if (char1 =='0' or char1 =='1') and (char2 =='0' or char2=='1'):
            output += char1 + '-'
        elif char1 ==')' and (char2 =='0' or char2=='1'):
            output += char1 +'-'
        elif (char1 =='0' or char1 =='1') and (char2 =='('):
            output += char1 +'-'
        elif char1 ==')' and char2 =='(':
            output += char1 +'-'
        elif char1 == '*' and (char2 =='0' or char2=='1'):
            output += char1 +'-'
        elif char1 == '*' and char2 =='(':
            output += char1 +'-'
        else:
            output += char1
            
    return output

