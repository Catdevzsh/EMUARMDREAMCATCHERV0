 
import re
from subprocess import Popen, PIPE

def compile_c(code):
    # Compile the C code to ARM assembly
    try:
        # Use GCC to compile the C code into an executable
        gcc = Popen(['gcc', '-o', 'a.out', '-xc', '-'], stdin=PIPE, stdout=PIPE)
        
        # Pass the C code as input to GCC
        gcc.communicate(code.encode())
        
        # Check if GCC was successful
        if gcc.returncode != 0:
            raise Exception("Compilation failed")
            
        # Use objdump to disassemble the executable into ARM assembly
        objdump = Popen(['objdump', '-d', 'a.out'], stdout=PIPE)
        
        # Extract only the ARM assembly part of the output
        arm_assembly = re.search(r'Disassembly of section \..*:\n.*\n(?:.*\n)*\n0\t[^\n]*', objdump.communicate()[0].decode()).group()
        
        # Remove the leading address and trailing newline characters
        arm_assembly = re.sub(r'^[0-9a-fA-F]+ <.*>:', '', arm_assembly)
        arm_assembly = re.sub(r'\n$', '', arm_assembly)
        
        # Return the ARM assembly code
        return arm_assembly
    except Exception as e:
        print("An error occurred:", str(e))
        return None

# Example usage
c_code = """
int main() {
    int a = 5;
    int b = 10;
    int c = a + b;
    printf("%d\\n", c);
    return 0;
}
"""

arm_assembly = compile_c(c_code)
if arm_assembly:
    print("ARM Assembly Code:\n", arm_assembly)
else:
    print("Compilation failed")
 
