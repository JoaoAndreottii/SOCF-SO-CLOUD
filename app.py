import os
import platform
import psutil
from flask import Flask, jsonify, render_template

xapp = Flask(__name__)

def xget_system_info():
    """Coleta informações do sistema"""
    xprocess = psutil.Process(os.getpid())
    

    xpid = os.getpid()
    xmemory_mb = xprocess.memory_info().rss / (1024 * 1024)
    xcpu_percent = xprocess.cpu_percent(interval=0.1)
    
    xos_name = platform.system()
    
    try:
        import distro
        xdistro_name = distro.name()
        xos_info = f"{xos_name} ({xdistro_name})"
    except:
        xos_info = xos_name
    
    return {
        "pid": xpid,
        "memoria_mb": round(xmemory_mb, 2),
        "cpu_percent": xcpu_percent,
        "sistema_operacional": xos_info
    }

@xapp.route('/')
def xhome():
    """Página principal com todas as informações"""
    xinfo = xget_system_info()
    xinfo['nome'] = 'João Otávio Andreotti'
    return render_template('index.html', info=xinfo)

@xapp.route('/info')
def xinfo_route():
    """Rota que retorna apenas o nome dos integrantes em JSON"""
    return jsonify({
        "nome": "João Otávio Andreotti"
    })

@xapp.route('/metricas')
def xmetricas():
    """Rota que retorna todas as métricas em JSON"""
    xinfo = xget_system_info()
    xinfo['nome'] = 'João Otávio Andreotti'
    return jsonify(xinfo)

APP = xapp

if __name__ == '__main__':
    xapp.run(debug=True, host='0.0.0.0', port=5000)