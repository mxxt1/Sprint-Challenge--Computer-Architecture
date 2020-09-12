"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = self.reg[7] = 0xF4
        self.L = 0
        self.G = 0
        self.E = 0
        self.FL = f'{self.L}{self.G}{self.E}'



    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        '''
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        '''
        program = []
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split('#', 1)[0]
                        line = int(line, 2)          
                        program.append(line)
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f'Couldnt find file {sys.argv[1]}')
            sys.exit(1)
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')


    def run(self):
        """Run the CPU."""
        running = True
        while running:
            inst = self.ram[self.pc]
            if inst == 130:                 # this is LDI, saving the number to reg
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif inst == 71:               # this is PRN, printing the number
                reg_index = self.ram[self.pc + 1]
                print(self.reg[reg_index])
                self.pc += 1
            elif inst == 1:                #  this is to stop running
                running = False
            elif inst == 162:                # this is MUL, multiplying the two numbers
                firstNum = self.ram[self.pc + 1]
                secondNum = self.ram[self.pc + 2]
                answer = self.reg[firstNum] * self.reg[secondNum]
                self.reg[firstNum] = answer
                self.pc += 3
            elif inst == 69:               # push
                self.sp -= 1
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                push_address = self.sp
                self.ram[push_address] = value
                self.pc += 2
            elif inst == 70:               # pop
                pop_address = self.sp
                value = self.ram[pop_address]
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value
                self.sp += 1
                self.pc += 2
            elif inst == 80:                # call
                return_address = self.pc + 2
                self.reg[7] -= 1
                push_address = self.reg[7]
                self.ram[push_address] = return_address
                reg_num = self.ram[self.pc+1]
                subroutine_addr = self.reg[reg_num]
                self.pc = subroutine_addr
            elif inst == 17:                # return
                pop_address = self.reg[7]
                return_address = self.ram[pop_address]
                self.pc = return_address
            elif inst == 160:               # add
                first_num = self.ram[self.pc + 1]
                second_num = self.ram[self.pc + 2]
                answer = self.reg[first_num] + self.reg[second_num]
                self.reg[first_num] = answer
                self.pc += 3



            #CMP    
            elif inst == 167:
                first_num = self.ram[self.pc + 1]
                second_num = self.ram[self.pc + 2]
                if self.reg[first_num] == self.reg[second_num]:
                    self.E = 1
                elif self.reg[first_num] < self.reg[second_num]:
                    self.L = 1
                elif self.reg[first_num] > self.reg[second_num]:
                    self.G = 1
                self.pc += 3


    def ram_read(self, MAR):
        return self.ram[MAR]
        
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return self.ram[MAR]