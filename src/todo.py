"""lista de tarefas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tarefas.json"


def carregar() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def salvar(tarefas: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(tarefas, ensure_ascii=False, indent=2), encoding="utf-8")


def adicionar(titulo: str) -> None:
    tarefas = carregar()
    novo_id = (max((t["id"] for t in tarefas), default=0) + 1)
    tarefas.append({"id": novo_id, "titulo": titulo, "concluida": False})
    salvar(tarefas)
    print(f"Tarefa #{novo_id} adicionada: {titulo}")


def listar() -> None:
    tarefas = carregar()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for t in tarefas:
        marca = "[x]" if t["concluida"] else "[ ]"
        print(f"{marca} {t['id']}. {t['titulo']}")


def concluir(tarefa_id: int) -> None:
    tarefas = carregar()
    for t in tarefas:
        if t["id"] == tarefa_id:
            t["concluida"] = True
            salvar(tarefas)
            print(f"Tarefa #{tarefa_id} concluída.")
            return
    print(f"Tarefa #{tarefa_id} não encontrada.", file=sys.stderr)
    sys.exit(1)


def ajuda() -> None:
    print("Uso: python src/todo.py <comando> [argumentos]")
    print("Comandos disponíveis:\n  add <titulo>  cadastra uma tarefa\n  list          lista as tarefas\n  done <id>     marca como concluída")


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        ajuda()
        sys.exit(1)
    comando = argv[1]
    if comando == "add" and len(argv) >= 3:
        adicionar(" ".join(argv[2:]))
    elif comando == "list":
        listar()
    elif comando == "done" and len(argv) >= 3:
        concluir(int(argv[2]))
    else:
        ajuda()
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
