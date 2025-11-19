# carreiras.py
# Sistema Simples de Orientação de Carreiras (Monolítico e Funcional)

import os
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# --- 1. CONFIGURAÇÃO E DADOS ---
MIN_SCORE, MAX_SCORE, GAP_TH, HIGH_W_TH = 1, 5, 4, 20

@dataclass(frozen=True)
class CInfo:
    nome: str
    desc: str
    sugestao: str

@dataclass(frozen=True)
class Carreira:
    nome: str
    pesos: Dict[str, int]

@dataclass
class Perfil:
    nome: str
    skills: Dict[str, int] = field(default_factory=dict)

@dataclass
class Relatorio:
    carreira_nome: str
    match_perc: float
    gaps: List[Dict[str, str]]

DB_C: Dict[str, CInfo] = {
    'logica': CInfo('Lógica', 'Raciocínio estruturado.', 'Estude Algoritmos.'),
    'criatividade': CInfo('Criatividade', 'Inovação e ideias novas.', 'Pratique Design Thinking.'),
    'colaboracao': CInfo('Colaboração', 'Trabalho em equipe.', 'Participe de projetos Open Source.'),
    'adaptabilidade': CInfo('Adaptabilidade', 'Resiliência a mudanças.', 'Aprenda uma tecnologia nova.'),
    'dados': CInfo('Análise de Dados', 'Interpretação estatística.', 'Domine Pandas e SQL.'),
    'automacao': CInfo('Automação', 'Otimização de processos.', 'Crie scripts Python.'),
    'etica': CInfo('Ética Digital', 'Responsabilidade e segurança.', 'Estude LGPD e vieses em IA.')
}
DB_CARREIRAS: List[Carreira] = [
    Carreira('Engenheiro de ML', {'logica': 30, 'dados': 30, 'automacao': 20, 'adaptabilidade': 10, 'etica': 10}),
    Carreira('Product Designer (UX/UI)', {'criatividade': 40, 'colaboracao': 20, 'adaptabilidade': 15, 'logica': 10}),
    Carreira('DevOps & SRE', {'automacao': 35, 'logica': 25, 'colaboracao': 20, 'etica': 20}),
]
def get_chaves(): return list(DB_C.keys())

# --- 2. MOTOR DE RECOMENDAÇÃO ---
class Motor:
    def __init__(self, perfil: Perfil):
        self.perfil = perfil

    def _afinidade(self, pesos: Dict[str, int]) -> float:
        chaves = list(pesos.keys())
        notas = np.array([self.perfil.skills.get(c, 0) for c in chaves])
        pesos_arr = np.array([pesos[c] for c in chaves])

        # Cálculo Ponderado (NumPy)
        notas_norm = notas / MAX_SCORE 
        score_total = np.sum(notas_norm * pesos_arr)
        peso_total = np.sum(pesos_arr)

        return (score_total / peso_total) * 100 if peso_total else 0.0

    def _gaps(self, pesos: Dict[str, int]) -> List[Dict[str, str]]:
        gaps = []
        for chave, peso in sorted(pesos.items(), key=lambda x: x[1], reverse=True):
            nota = self.perfil.skills.get(chave, 0)
            
            if peso >= HIGH_W_TH and nota < GAP_TH:
                info = DB_C.get(chave)
                if info:
                    gaps.append({
                        "competencia": info.nome,
                        "nota_atual": str(nota),
                        "peso_na_carreira": str(peso),
                        "acao": info.sugestao
                    })
        return gaps

    def gerar_analise(self) -> List[Relatorio]:
        resultados = []
        for carreira in DB_CARREIRAS:
            afinidade = self._afinidade(carreira.pesos)
            gaps = self._gaps(carreira.pesos)
            
            resultados.append(Relatorio(carreira.nome, afinidade, gaps))

        resultados.sort(key=lambda x: x.match_perc, reverse=True)
        return resultados

# --- 3. INTERFACE (CLI) ---
def limpar(): os.system('cls' if os.name == 'nt' else 'clear')

def input_valido(prompt: str, tipo=int, min_v: Optional[int]=None, max_v: Optional[int]=None):
    while True:
        try:
            valor = tipo(input(prompt))
            if min_v is not None and valor < min_v: continue
            if max_v is not None and valor > max_v: continue
            return valor
        except ValueError: pass

def coletar_dados() -> Perfil:
    nome = input("Digite seu nome: ").strip()
    perfil = Perfil(nome)
    
    print(f"\nOlá, {nome}! Avalie de {MIN_SCORE} (Fraco) a {MAX_SCORE} (Forte).\n")
    
    for chave in get_chaves():
        info = DB_C[chave] 
        print(f" -> {info.nome.upper()} ({info.desc})")
        nota = input_valido(f"   Nota ({MIN_SCORE}-{MAX_SCORE}): ", min_v=MIN_SCORE, max_v=MAX_SCORE)
        perfil.skills[chave] = nota
        print("-" * 40)
        
    return perfil

def apresentar_relatorio(nome: str, analises: List[Relatorio]):
    limpar()
    print("="*60)
    print(f" RESULTADOS PARA: {nome.upper()}")
    print("="*60)

    top = analises[0]
    print(f"\n🏆 RECOMENDAÇÃO PRINCIPAL: {top.carreira_nome}")
    print(f" Match de Perfil: {top.match_perc:.1f}%")
    
    if top.gaps:
        print("\n⚠️  PONTOS DE ATENÇÃO (Aprimoramento):")
        for gap in top.gaps:
            print(f"   • {gap['competencia']} (Sua Nota: {gap['nota_atual']})")
            print(f"     Ação: {gap['acao']}")
    else:
        print("\n✅ Perfil Altamente Compatível!")

    print("\n" + "-"*60)
    print("Outras Opções:")
    for analise in analises[1:]:
        print(f"   • {analise.carreira_nome}: {analise.match_perc:.1f}%")
    
    print("="*60 + "\n")

def main():
    limpar()
    print("=== Sistema Simples de Carreiras ===")
    
    try:
        perfil = coletar_dados()
        motor = Motor(perfil)
        analises = motor.gerar_analise()
        
        apresentar_relatorio(perfil.nome, analises)
        
    except KeyboardInterrupt:
        print("\n\nSistema encerrado.")
    except Exception as e:
        print(f"\n Erro crítico: {e}")
        print("Certifique-se de que o NumPy está instalado: pip install numpy")

if __name__ == "__main__":
    main()