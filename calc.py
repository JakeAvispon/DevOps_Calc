from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = None
    # Por defecto, si apenas entras a la página, es 'simple'
    current_mode = 'simple' 
    
    if request.method == 'POST':
        try:
            # Capturamos el modo en el que estábamos al darle a "Convertir"
            current_mode = request.form.get('calc_mode', 'simple')
            n1 = int(request.form.get('n1', 0))
            
            if current_mode == 'simple':
                res = {'type': 'simple', 'val': bin(n1)}
                
            elif current_mode == 'operation':
                n2 = int(request.form.get('n2', 0))
                op = request.form.get('op')
                
                if op == 'sum': raw = n1 + n2
                elif op == 'sub': raw = n1 - n2
                elif op == 'mul': raw = n1 * n2
                elif op == 'div': raw = n1 // n2 if n2 != 0 else 0
                
                res = {
                    'type': 'op',
                    'bin1': bin(n1),
                    'bin2': bin(n2),
                    'bin_res': bin(raw),
                    'dec_res': raw
                }
                
            elif current_mode == 'logical':
                n2_raw = request.form.get('n2')
                n2 = int(n2_raw) if n2_raw else 0
                op = request.form.get('op')
                
                if op == 'and': raw = n1 & n2
                elif op == 'or': raw = n1 | n2
                elif op == 'xor': raw = n1 ^ n2
                elif op == 'not': raw = ~n1
                
                res = {
                    'type': 'logical',
                    'op_name': op.upper(),
                    'bin1': bin(n1),
                    'bin2': bin(n2) if op != 'not' else 'N/A (Ignorado)',
                    'bin_res': bin(raw),
                    'dec_res': raw
                }
        except:
            res = {'error': 'Datos inválidos o campos vacíos'}

    # Le pasamos a la plantilla HTML el resultado y el modo en el que estábamos
    return render_template('index.html', result=res, current_mode=current_mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)