# 🤖 Integración de IA (CHAT-GPT) con Arduino mediante Python: Ejemplo Educativo

## 📝 Descripción

Este proyecto es un ejemplo base diseñado para mostrar a los alumnos cómo llevar a cabo integraciones y retroalimentaciones entre la Inteligencia Artificial, en este caso CHAT-GPT, y el hardware actual, representado por Arduino. A través de Python, que actúa como puente entre ambas tecnologías, el código solicita a CHAT-GPT el código necesario para hacer funcionar un circuito montado en la placa Arduino. Tomamos como referencia el ejemplo [Blink](https://docs.arduino.cc/built-in-examples/basics/Blink) de la documentación oficial de Arduino. Si la placa devuelve una respuesta negativa tras la compilación, el proceso se repite de manera recursiva solicitando a CHAT-GPT hasta obtener una respuesta de compilación correcta.

Este proyecto tiene fines educativos y busca proporcionar a los estudiantes una comprensión clara de cómo las tecnologías de Inteligencia Artificial pueden interactuar y complementar al hardware tradicional.

## 🌟 Características

- **Enfoque Educativo**: Diseñado para ser un recurso didáctico para estudiantes interesados en la integración de IA y hardware.
- **Integración con CHAT-GPT**: Muestra cómo utilizar la IA para obtener el código necesario para un circuito.
- **Automatización y Retroalimentación**: Enseña cómo manejar errores y solicitar automáticamente correcciones a la IA.
- **Flexibilidad**: Aunque se basa en el ejemplo Blink, el proyecto puede adaptarse para otros circuitos y necesidades.

## 🛠 Requisitos

- Python 3.x
- Biblioteca PySerial para comunicación con Arduino
- Placa Arduino

## 🚀 Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt

## 📖 Uso

1. Conecta tu placa Arduino a tu computadora.
2. Modifica los valores del archivo ardu-gpt.py necesarios para tu placa Arduino (linea 106)
3. Modifica el valor del prompt para CHAT-GPT en el archivo ardu-gpt.py en funcion de tu circuito a resolver (linea 111)
4. Ejecuta el script principal:
   ```bash
   python ardu-gpt.py

Al ejecutar el script, este solicitará automáticamente a CHAT-GPT el código para el circuito. Si la compilación es exitosa, verás un mensaje de éxito. De lo contrario, el sistema intentará nuevamente hasta obtener un código válido.

![Demo running GIF](https://github.com/404-OS/ardu-gpt/blob/main/demo_gif.gif)

## 🤝 Contribuciones
Las contribuciones son bienvenidas, especialmente si tienen un enfoque educativo. Si tienes sugerencias, correcciones o mejoras, no dudes en hacer un pull request o abrir un issue.

## 📜 Licencia
Este proyecto está bajo la licencia GNU GENERAL PUBLIC LICENSE V3. Consulta el archivo LICENSE para más detalles.