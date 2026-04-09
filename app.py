from flask import Flask, render_template_string, send_file, request
import random
import datetime
import io
import uuid
import re

app = Flask(__name__)

LISTA_BANCOS = [
    {"code": "341", "name": "ITAÚ UNIBANCO S.A."},
    {"code": "616", "name": "MARVEL_DC_FINANCE"},
    {"code": "001", "name": "BANCO DO BRASIL S.A."},
    {"code": "237", "name": "BANCO BRADESCO S.A."}
]

# Lista de fornecedores para massa de dados
FORNECEDORES_MASSA = [
    {"id":728,"corporate_name":"BANCO DO BRASIL S.A.","cnpj":"00.000.000/0001-91"},
    {"id":729,"corporate_name":"BANCO BRADESCO S.A.","cnpj":"60.746.948/0001-12"},
    {"id":730,"corporate_name":"BANCO CITIBANK S.A.","cnpj":"33.479.023/0001-80"},
    {"id":731,"corporate_name":"BANCO DAYCOVAL S.A.","cnpj":"62.232.889/0001-44"},
    {"id":732,"corporate_name":"BANCO COOPERATIVO DO BRASIL S.A. - BANCOOB","cnpj":"02.038.232/0001-42"},
    {"id":733,"corporate_name":"BANCO COOPERATIVO SICREDI S.A.","cnpj":"01.181.521/0001-55"},
    {"id":734,"corporate_name":"BANCO DO ESTADO DO RIO GRANDE DO SUL S.A.","cnpj":"92.702.067/0001-96"},
    {"id":735,"corporate_name":"GLOBO COMUNICACAO E PARTICIPACOES S/A","cnpj":"27.865.757/0001-02"},
    {"id":736,"corporate_name":"TELEFONICA BRASIL S.A.","cnpj":"00.000.000/0001-01"},
    {"id":737,"corporate_name":"CLARO S.A.","cnpj":"02.449.992/0001-64"},
    {"id":738,"corporate_name":"TELEMAR NORTE LESTE S.A.","cnpj":"33.000.118/0001-79"},
    {"id":739,"corporate_name":"TIM S.A.","cnpj":"05.423.963/0001-11"},
    {"id":740,"corporate_name":"COOPERCITRUS COOPERATIVA","cnpj":"61.088.594/0001-18"},
    {"id":741,"corporate_name":"RAIZEN ENERGIA S.A.","cnpj":"43.214.055/0001-07"},
    {"id":742,"corporate_name":"PETROLEO BRASILEIRO S.A.","cnpj":"33.000.167/0001-01"},
    {"id":743,"corporate_name":"AMBEV S.A.","cnpj":"07.164.139/0001-03"},
    {"id":744,"corporate_name":"NESTLE BRASIL LTDA.","cnpj":"60.621.141/0001-28"},
    {"id":745,"corporate_name":"MINISTERIO DA FAZENDA","cnpj":"00.394.460/0001-41"},
    {"id":746,"corporate_name":"COPEL DISTRIBUICAO S.A.","cnpj":"76.483.817/0001-20"},
    {"id":747,"corporate_name":"ENEL DISTRIBUICAO","cnpj":"61.695.227/0001-93"},
    {"id":748,"corporate_name":"SABESP S.A.","cnpj":"04.172.213/0001-51"},
    {"id":749,"corporate_name":"CORSAN S.A.","cnpj":"92.754.738/0001-62"},
    {"id":750,"corporate_name":"VALE S.A.","cnpj":"33.592.510/0001-54"},
    {"id":751,"corporate_name":"CCR S.A.","cnpj":"03.007.331/0001-41"},
    {"id":752,"corporate_name":"LOCALIZA RENT A CAR S.A.","cnpj":"02.558.157/0001-62"},
    {"id":753,"corporate_name":"WEG EQUIPAMENTOS ELETRICOS","cnpj":"02.851.873/0001-00"},
    {"id":754,"corporate_name":"KLABIN S.A.","cnpj":"60.850.229/0001-21"},
    {"id":755,"corporate_name":"SUZANO S.A.","cnpj":"16.404.287/0001-55"},
    {"id":756,"corporate_name":"BRF S.A.","cnpj":"60.390.699/0001-46"},
    {"id":757,"corporate_name":"JBS S.A.","cnpj":"02.914.460/0001-50"},
    {"id":758,"corporate_name":"MAGAZINE LUIZA S.A.","cnpj":"03.361.252/0001-34"},
    {"id":759,"corporate_name":"LOJAS RENNER S.A.","cnpj":"93.209.765/0001-17"},
    {"id":760,"corporate_name":"LOJAS AMERICANAS S.A.","cnpj":"00.776.574/0001-56"},
    {"id":761,"corporate_name":"VIA S.A.","cnpj":"23.643.315/0001-52"},
    {"id":762,"corporate_name":"CARREFOUR COMERCIO","cnpj":"45.543.915/0001-81"},
    {"id":763,"corporate_name":"GPA S.A.","cnpj":"75.315.333/0001-09"},
    {"id":764,"corporate_name":"LATAM AIRLINES","cnpj":"03.217.454/0001-10"},
    {"id":765,"corporate_name":"AZUL LINHAS AEREAS","cnpj":"02.575.829/0001-48"},
    {"id":766,"corporate_name":"GOL LINHAS AEREAS","cnpj":"07.575.651/0001-59"},
    {"id":767,"corporate_name":"B3 S.A.","cnpj":"09.346.601/0001-25"},
    {"id":768,"corporate_name":"CAIXA ECONOMICA","cnpj":"00.360.305/0001-04"},
    {"id":769,"corporate_name":"ITAÚ UNIBANCO S.A.","cnpj":"60.701.190/0001-04"},
    {"id":770,"corporate_name":"BANCO SANTANDER S.A.","cnpj":"90.400.888/0001-42"},
    {"id":771,"corporate_name":"NU PAGAMENTOS S.A.","cnpj":"17.298.092/0001-30"},
    {"id":772,"corporate_name":"BANCO INTER S.A.","cnpj":"18.236.120/0001-58"},
    {"id":773,"corporate_name":"BTG PACTUAL S.A.","cnpj":"07.450.604/0001-89"},
    {"id":774,"corporate_name":"XP INVESTIMENTOS","cnpj":"10.573.521/0001-91"},
    {"id":775,"corporate_name":"TOTVS S.A.","cnpj":"02.351.144/0001-18"},
    {"id":776,"corporate_name":"NATURA COSMETICOS","cnpj":"61.198.164/0001-60"},
    {"id":777,"corporate_name":"EDP BRASIL S.A.","cnpj":"11.137.051/0001-86"},
    {"id":778,"corporate_name":"EQUATORIAL ENERGIA","cnpj":"00.482.121/0001-19"},
    {"id":779,"corporate_name":"BRASKEM S.A.","cnpj":"01.838.723/0001-27"},
    {"id":780,"corporate_name":"ELETROBRAS S.A.","cnpj":"00.001.180/0001-26"},
    {"id":781,"corporate_name":"OI S.A. FIXO","cnpj":"02.429.144/0001-93"},
    {"id":782,"corporate_name":"REDE DOR SAO LUIZ","cnpj":"15.473.643/0001-10"},
    {"id":783,"corporate_name":"HAPVIDA ASSISTENCIA","cnpj":"61.533.584/0001-44"},
    {"id":784,"corporate_name":"SUL AMERICA S.A.","cnpj":"61.412.110/0001-55"},
    {"id":785,"corporate_name":"PORTO SEGURO S.A.","cnpj":"33.010.091/0001-31"},
    {"id":786,"corporate_name":"BB SEGURIDADE S.A.","cnpj":"00.306.495/0001-43"},
    {"id":787,"corporate_name":"COSAN S.A.","cnpj":"01.547.053/0001-11"},
    {"id":788,"corporate_name":"ULTRAPAR S.A.","cnpj":"10.231.547/0001-22"},
    {"id":789,"corporate_name":"CPFL ENERGIA S.A.","cnpj":"03.853.896/0001-40"},
    {"id":790,"corporate_name":"ENGIE BRASIL S.A.","cnpj":"01.018.550/0001-21"},
    {"id":791,"corporate_name":"COPEL SEDE","cnpj":"00.415.956/0001-85"},
    {"id":792,"corporate_name":"ASSAI ATACADISTA","cnpj":"06.057.223/0001-71"},
    {"id":793,"corporate_name":"ATACADAO S.A.","cnpj":"23.476.517/0001-80"},
    {"id":794,"corporate_name":"RAIA DROGASIL S.A.","cnpj":"01.527.322/0001-11"},
    {"id":795,"corporate_name":"MULTILASER S.A.","cnpj":"03.543.153/0001-20"},
    {"id":796,"corporate_name":"AREZZO INDUSTRIA","cnpj":"08.334.385/0001-35"},
    {"id":797,"corporate_name":"GRUPO SOMA S.A.","cnpj":"05.570.714/0001-59"},
    {"id":798,"corporate_name":"ALPARGATAS S.A.","cnpj":"02.474.103/0001-19"},
    {"id":799,"corporate_name":"GRENDENE S.A.","cnpj":"61.079.117/0001-05"},
    {"id":800,"corporate_name":"M. DIAS BRANCO S.A.","cnpj":"05.526.104/0001-22"},
    {"id":801,"corporate_name":"MINERVA S.A.","cnpj":"43.111.311/0001-01"},
    {"id":802,"corporate_name":"MARFRIG GLOBAL S.A.","cnpj":"01.505.050/0001-01"},
    {"id":803,"corporate_name":"SLC AGRICOLA S.A.","cnpj":"01.144.144/0001-01"},
    {"id":804,"corporate_name":"SAO MARTINHO S.A.","cnpj":"00.222.111/0001-01"},
    {"id":805,"corporate_name":"ALIANSCE SONAE S.A.","cnpj":"10.111.000/0001-01"},
    {"id":806,"corporate_name":"BRMALLS S.A.","cnpj":"00.333.444/0001-01"},
    {"id":807,"corporate_name":"IGUATEMI S.A.","cnpj":"05.000.111/0001-01"},
    {"id":808,"corporate_name":"MULTIPLAN S.A.","cnpj":"00.888.777/0001-01"},
    {"id":809,"corporate_name":"CYRELA REALTY S.A.","cnpj":"02.555.666/0001-01"},
    {"id":810,"corporate_name":"MRV ENGENHARIA S.A.","cnpj":"01.444.333/0001-01"},
    {"id":811,"corporate_name":"EZTEC S.A.","cnpj":"03.222.111/0001-01"},
    {"id":812,"corporate_name":"JHSF S.A.","cnpj":"04.111.000/0001-01"},
    {"id":813,"corporate_name":"ODONTOPREV S.A.","cnpj":"01.888.999/0001-01"},
    {"id":814,"corporate_name":"FLEURY S.A.","cnpj":"00.555.444/0001-01"},
    {"id":815,"corporate_name":"QUALICORP S.A.","cnpj":"02.111.333/0001-01"},
    {"id":816,"corporate_name":"YDUQS S.A.","cnpj":"00.999.888/0001-01"},
    {"id":817,"corporate_name":"COGNA EDUCACAO S.A.","cnpj":"01.666.555/0001-01"},
    {"id":818,"corporate_name":"PETZ S.A.","cnpj":"01.222.111/0001-01"},
    {"id":819,"corporate_name":"COBASI S.A.","cnpj":"02.333.444/0001-01"},
    {"id":820,"corporate_name":"RAIA S.A.","cnpj":"00.444.555/0001-01"},
    {"id":821,"corporate_name":"DROGASIL S.A.","cnpj":"00.555.666/0001-01"},
    {"id":822,"corporate_name":"PAGSEGURO S.A.","cnpj":"00.666.777/0001-01"},
    {"id":823,"corporate_name":"STONE CO S.A.","cnpj":"00.777.888/0001-01"},
    {"id":824,"corporate_name":"REDE S.A.","cnpj":"00.888.999/0001-01"},
    {"id":825,"corporate_name":"CIELO S.A.","cnpj":"00.999.000/0001-01"},
    {"id":826,"corporate_name":"GETNET S.A.","cnpj":"01.000.111/0001-01"},
    {"id":827,"corporate_name":"PAGBANK S.A.","cnpj":"01.111.222/0001-01"}
]


HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>OFX Ultra Generator | Stratexa</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #020617; }
        .card { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-6 text-white">
    <div class="w-full max-w-lg card p-10 rounded-[2.5rem] shadow-2xl border-t-4 border-cyan-500">
        <h1 class="text-2xl font-black mb-8 text-center text-cyan-400 uppercase tracking-tighter">
            OFX Smart Generator
        </h1>
        <form action="/gerar-ofx" method="GET" class="space-y-6">
            <div class="p-4 bg-slate-900/50 rounded-2xl border border-slate-700">
                <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">CNPJ da Empresa Principal (Emissora)</label>
                <input type="text" name="cnpj_principal" placeholder="00.000.000/0001-00" value="19.943.789/0001-42" class="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 px-4 text-cyan-400 font-mono mb-4">
                
                <label class="block text-[10px] font-bold text-slate-500 uppercase mb-1">Banco</label>
                <select name="banco_index" class="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 px-4 text-cyan-400 font-bold mb-4">
                    {% for banco in bancos %}
                    <option value="{{ loop.index0 }}">{{ banco.code }} - {{ banco.name }}</option>
                    {% endfor %}
                </select>
                <div class="grid grid-cols-3 gap-3">
                    <input type="text" name="agencia" placeholder="Agência" value="0001" class="bg-slate-900 border border-slate-700 rounded-xl py-3 text-center text-xs">
                    <input type="text" name="conta" value="83241" class="bg-slate-900 border border-slate-700 rounded-xl py-3 text-center text-xs">
                    <input type="text" name="digito" value="0" class="bg-slate-900 border border-slate-700 rounded-xl py-3 text-center text-xs">
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4 p-4 bg-emerald-500/5 rounded-2xl border border-emerald-500/20">
                <div>
                    <label class="block text-xs font-bold text-emerald-400 uppercase mb-2 text-center text-[10px]">Quantidade</label>
                    <input type="number" name="qtd" value="10" class="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 text-xl font-black text-emerald-400 text-center">
                </div>
                <div>
                    <label class="block text-xs font-bold text-emerald-400 uppercase mb-2 text-center text-[10px]">Valor (Opcional)</label>
                    <input type="text" name="valor_fixo" placeholder="Ex: 100.50" class="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 text-xl font-black text-emerald-400 text-center">
                </div>
            </div>

            <div class="p-4 bg-blue-500/5 rounded-2xl border border-blue-500/20">
                <label class="block text-[10px] font-bold text-blue-400 uppercase mb-2">Data da OFX (Opcional)</label>
                <input type="date" name="data_ofx" class="w-full bg-slate-900 border border-slate-700 rounded-xl py-3 px-4 text-blue-400 font-mono">
            </div>

            <div class="grid grid-cols-2 gap-4">
                <button type="submit" name="tipo_fluxo" value="DEBIT" class="bg-red-600 hover:bg-red-500 text-white font-black py-5 rounded-2xl uppercase shadow-lg shadow-red-900/20 transition-all active:scale-95">SÓ DÉBITO (-)</button>
                <button type="submit" name="tipo_fluxo" value="CREDIT" class="bg-emerald-600 hover:bg-emerald-500 text-white font-black py-5 rounded-2xl uppercase shadow-lg shadow-emerald-900/20 transition-all active:scale-95">SÓ CRÉDITO (+)</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT, bancos=LISTA_BANCOS)

@app.route('/gerar-ofx')
def gerar_ofx():
    # Parâmetros
    idx = int(request.args.get('banco_index', 0))
    banco = LISTA_BANCOS[idx]
    tipo_fluxo = request.args.get('tipo_fluxo', 'DEBIT')
    qtd = int(request.args.get('qtd', 10))
    
    # Captura e limpeza do CNPJ (remove qualquer caractere que não seja número)
    cnpj_raw = request.args.get('cnpj_principal', '').strip()
    cnpj_limpo = re.sub(r'\D', '', cnpj_raw) 
    
    valor_fixo_raw = request.args.get('valor_fixo', '').replace(',', '.')
    valor_fixo = float(valor_fixo_raw) if valor_fixo_raw else None
    
    agencia = request.args.get('agencia', '0001').strip()
    conta = request.args.get('conta', '83241').strip()
    digito = request.args.get('digito', '0').strip()
    
    # Identificadores
    acctid_valor = f"{conta}{digito}"  # Concatena conta + dígito
    org_valor = banco['name']  # Usa o nome do banco

    # Data da OFX (se fornecida, converte; caso contrário usa agora)
    data_ofx_str = request.args.get('data_ofx', '').strip()
    if data_ofx_str:
        now = datetime.datetime.strptime(data_ofx_str, '%Y-%m-%d').replace(hour=23, minute=59, second=0)
    else:
        now = datetime.datetime.now()
    dt_server = now.strftime('%Y%m%d%H%M%S')
    trnuid = f"REQ-{uuid.uuid4().hex[:10].upper()}"
    
    ofx_content = [
        "OFXHEADER:100", "DATA:OFXSGML", "VERSION:102", "SECURITY:NONE", "ENCODING:USASCII", "CHARSET:1252",
        "<OFX>", "  <SIGNONMSGSRSV1>", "    <SONRS>",
        "      <STATUS><CODE>0<SEVERITY>INFO</STATUS>",
        f"      <DTSERVER>{dt_server}", "      <LANGUAGE>POR",
        f"      <FI><ORG>{org_valor}<FID>{banco['code']}</FI>",
        "    </SONRS>", "  </SIGNONMSGSRSV1>",
        "  <BANKMSGSRSV1>", "    <STMTTRNRS>",
        f"      <TRNUID>{trnuid}",
        "      <STATUS><CODE>0<SEVERITY>INFO</STATUS>",
        "      <STMTRS>", "        <CURDEF>BRL",
        "        <BANKACCTFROM>",
        f"          <BANKID>{banco['code']}",
        f"          <BRANCHID>{agencia}",
        f"          <ACCTID>{acctid_valor}",
        "          <ACCTTYPE>CHECKING",
        "        </BANKACCTFROM>",
        "        <BANKTRANLIST>",
        f"          <DTSTART>{now.strftime('%Y%m%d000000')}",
        f"          <DTEND>{now.strftime('%Y%m%d235959')}"
    ]

    for i in range(qtd):
        f = random.choice(FORNECEDORES_MASSA)
        dt_post = (now - datetime.timedelta(minutes=i*2)).strftime('%Y%m%d%H%M%S')
        fitid = f"TRX{uuid.uuid4().hex[:14].upper()}"
        
        # Define o valor numérico
        if valor_fixo is not None:
            valor_calculado = valor_fixo
        else:
            valor_calculado = round(100 + random.random() * 500, 2)
        
        # FORMATAÇÃO FIXA: ".2f" garante 2 casas decimais (ex: 5.00 em vez de 5.0)
        if tipo_fluxo == "DEBIT":
            valor_str = f"-{valor_calculado:.2f}"
            memo = f"PGTO {f['corporate_name']}"
        else:
            valor_str = f"{valor_calculado:.2f}"
            memo = f"REC {f['corporate_name']}"

        ofx_content.append("          <STMTTRN>")
        ofx_content.append(f"            <TRNTYPE>{tipo_fluxo}")
        ofx_content.append(f"            <DTPOSTED>{dt_post}")
        ofx_content.append(f"            <TRNAMT>{valor_str}")
        ofx_content.append(f"            <FITID>{fitid}")
        ofx_content.append(f"            <CHECKNUM>{random.randint(100000, 999999)}")
        ofx_content.append(f"            <MEMO>{memo}")
        ofx_content.append("          </STMTTRN>")

    ofx_content.extend([
        "        </BANKTRANLIST>", "        <LEDGERBAL>", 
        f"          <BALAMT>{random.randint(5000, 20000)}",
        f"          <DTASOF>{now.strftime('%Y%m%d235959')}", "        </LEDGERBAL>",
        "      </STMTRS>", "    </STMTTRNRS>", "  </BANKMSGSRSV1>", "</OFX>"
    ])

    ofx_final = "\n".join(ofx_content)
    mem_file = io.BytesIO()
    mem_file.write(ofx_final.encode('utf-8'))
    mem_file.seek(0)
    
    return send_file(mem_file, as_attachment=True, download_name=f"extrato_{uuid.uuid4().hex[:4].upper()}.ofx", mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, port=4000)