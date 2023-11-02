import os, sys
import time
import serial
import openai
import subprocess
from OSExec import OSManager

class ARDUGPT:
    
    def __init__(self):
        self.os_exec_manager = OSManager()
        self.arduino_port = str() # Puerto COM
        self.arduino_velocity = int() # Velocidad de transeferencia de datos
        self.arduino_conn = False # Conexion con la placa arduino
        self.arduino_fqbn = str() # Arduino FQBN
        self.gpt_prompt = str() # Prompt a usar con Chat-GPT
        self.skecth_codes_path = str(os.getcwd()).replace('\\', '/')+'/sketch_code/' # Path para los archivos sketch
        self.sketch_codes_name = str('sketch_code.ino') # Nombre de los archivos creados
    
    # Conexion con Arduino
    def get_conn(self):
        try:
            self.arduino_conn = serial.Serial(self.arduino_port, self.arduino_velocity)
            return True
        except Exception as e:
            return False
    
    # Crear codigo Sketch con CHAT-GPT
    def get_chatgpt_code(self, prompt):
        print("[+] Generando codigo con GPT")
        openai.api_key = "your-gpt-api-key"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    # Guardar el codigo sketch generado
    def save_sketch_code(self, sketch_code):
        file = open(self.skecth_codes_path+'/'+self.sketch_codes_name, 'w')
        file.write(sketch_code)
        file.close()
        print("[+] Sketch creado: "+self.skecth_codes_path+self.sketch_codes_name)

    # Leer codigo Sketch creado
    def read_sketch_file_data(self):
        with open(self.skecth_codes_path+self.sketch_codes_name, 'r') as sketch_file:
            sketch_code = sketch_file.read()
        return sketch_code

    # Compila el sketch con arduino-cli
    def compile_sketch(self):
        compile_command = "arduino-cli compile --verbose --fqbn "+self.arduino_fqbn+" "+self.skecth_codes_path+" --output-dir "+self.skecth_codes_path
        #print(compile_command)
        res = self.os_exec_manager.executeCMD(compile_command, clear_data=False)
        return res

    # Carga el sketch en el Arduino
    def compiled_sketch_to_arduino(self):
        upload_command = 'arduino-cli upload --port '+self.arduino_port+' --fqbn '+self.arduino_fqbn+' --input-file '+self.skecth_codes_path+self.sketch_codes_name+'.hex'
        #print(upload_command)
        res = self.os_exec_manager.executeCMD(upload_command, clear_data=False, new_shell=True)
        return res

    # Enviar datos a placa Arduino
    def data_to_arduino_board(self, data):
        self.arduino_conn.write(data.encode())
        time.sleep(30)
        response = ''
        while self.arduino_conn.inWaiting() > 0:
            response += self.arduino_conn.read(1).decode()
        return response
    
    # Creacion de codigo automatica
    def run_agent(self):
        while True:
            # Codigo creado por GPT
            gpt_code = self.get_chatgpt_code(self.gpt_prompt)
            
            # Guardar codigo
            self.save_sketch_code(str(gpt_code).replace('`',''))
            
            # Compilar codigo
            compiler_res = self.compile_sketch()
            if compiler_res != False:
                print("[+] Sketch compilado")
                break
            else:
                print("[-] Error al compilar el Sketch")
        
        # Subida de codigo a la placa Arduino
        upload_res = self.compiled_sketch_to_arduino()
        if upload_res == False:
            print("[-] Error cargando el Sketch en la placa arduino")
        else:
            print("[+] Sketch Cargado")

        # Exit Agent
        return True

## USO ##
ardu_gpt_agent = ARDUGPT()

# PLACA ARDUINO
ardu_gpt_agent.arduino_port = str('COM5') # Puerto COM (Verificar usando )
ardu_gpt_agent.arduino_velocity = int(9600) # Velocidad de transeferencia de datos
ardu_gpt_agent.arduino_fqbn = str('arduino:avr:mega:cpu=atmega2560') # Arduino FQBN

# CHAT-GPT PROMPT
ardu_gpt_agent.gpt_prompt = str('Crea el codigo sketch.ino necesario para encender un led cada 1 segundo, respondeme solo con el codigo sketch sin añadir ninguna cabecera o palabra mas')

# INICIAR EL AGENTE
ardu_gpt_agent.run_agent() # Iniciar el agente