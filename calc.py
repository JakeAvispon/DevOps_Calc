from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = None
    if request.method == 'POST':
        try:
            mode = request.form.get('calc_mode')
            n1 = int(request.form.get('n1', 0))
            
            if mode == 'simple':
                res = {'type': 'simple', 'val': bin(n1)}
            else:
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
        except:
            res = {'error': 'Datos inválidos'}

    return render_template('index.html', result=res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)