"""
Interface web do chatbot BolsaCerta (só biblioteca padrão do Python).

    python web.py            -> abre http://localhost:8000 no navegador
    python web.py --porta 9000 --sem-navegador
"""

import argparse
import json
import secrets
import threading
import webbrowser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bolsacerta import AgenteBolsaCerta

PAGINA = Path(__file__).parent / "web" / "index.html"
SESSOES: dict[str, AgenteBolsaCerta] = {}
TRAVA = threading.Lock()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # terminal limpo durante a apresentação

    def _sessao(self):
        cookie = SimpleCookie(self.headers.get("Cookie"))
        sid = cookie["sid"].value if "sid" in cookie else None
        nova = sid not in SESSOES
        if nova:
            sid = secrets.token_hex(8)
            SESSOES[sid] = AgenteBolsaCerta()
        return sid, SESSOES[sid], nova

    def _json(self, dados, sid=None):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        if sid:
            self.send_header("Set-Cookie", f"sid={sid}; Path=/; HttpOnly; SameSite=Strict")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        corpo = PAGINA.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = json.loads(self.rfile.read(tamanho) or b"{}")
        with TRAVA:
            if self.path == "/api/reiniciar":
                sid = secrets.token_hex(8)
                SESSOES[sid] = AgenteBolsaCerta()
                bia = SESSOES[sid]
                resposta = bia.processar("oi")
                self._json({"resposta": resposta, "rastro": bia.ultimo_rastro}, sid)
            elif self.path == "/api/mensagem":
                sid, bia, nova = self._sessao()
                texto = str(dados.get("texto", ""))[:500].strip() or "oi"
                resposta = bia.processar(texto)
                self._json({"resposta": resposta, "rastro": bia.ultimo_rastro}, sid if nova else None)
            else:
                self.send_error(404)


def main():
    parser = argparse.ArgumentParser(description="Interface web do BolsaCerta")
    parser.add_argument("--porta", type=int, default=8000)
    parser.add_argument("--sem-navegador", action="store_true")
    args = parser.parse_args()

    servidor = ThreadingHTTPServer(("127.0.0.1", args.porta), Handler)
    url = f"http://localhost:{args.porta}"
    print(f"BolsaCerta rodando em {url}  (Ctrl+C para parar)")
    if not args.sem_navegador:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")


if __name__ == "__main__":
    main()
