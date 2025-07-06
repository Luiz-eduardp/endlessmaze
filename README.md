# Endless Maze - Um Jogo de Labirinto Retrô

![Gameplay do Endless Maze](/assets/image.png)

**Endless Maze** é um jogo 2D desafiador onde o objetivo é navegar por labirintos gerados processualmente antes que o tempo acabe. A cada nível, os labirintos se tornam maiores, o tempo fica mais curto e mais inimigos aparecem no seu caminho. Com uma estética nostálgica inspirada no Game Boy, o jogo oferece um desafio simples, viciante e infinito.

---

## ✨ Funcionalidades

- **Níveis Infinitos:** Jogue o quanto quiser! Um novo labirinto é gerado toda vez que você encontra a saída.
- **Labirintos Gerados Processualmente:** Nunca jogue o mesmo labirinto duas vezes. O algoritmo de *Recursive Backtracking* garante um layout único a cada nível.
- **Dificuldade Progressiva:** A cada nível, o desafio aumenta:
  - Os labirintos ficam maiores e mais complexos.
  - O tempo para encontrar a saída diminui.
  - O número de inimigos aumenta.
- **Estética Retrô :** Paleta de cores e design de sprites que remetem aos jogos clássicos portáteis.
- **Controles Simples e Responsivos:** Fácil de aprender, com uma movimentação fluida graças ao sistema de hitbox que evita prender nas paredes.

---

## 🚀 Como Jogar

Para rodar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
- `pip` (geralmente instalado com o Python)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd seu-repositorio
    ```

3.  **Instale as dependências (Pygame):**
    ```bash
    pip install pygame
    ```

4.  **Execute o jogo:**
    ```bash
    python main.py
    ```

---

## 🎮 Controles

- **Movimento:**
  - `Setas Direcionais` ou `W`, `A`, `S`, `D`

- **Jogo:**
  - `ESC`: Fecha o jogo.
  - `R`: Reinicia o jogo após um "Game Over".

---
## 🤝 Como Contribuir

Contribuições são sempre bem-vindas! Se você tiver ideias para novas funcionalidades, melhorias ou encontrar algum bug, sinta-se à vontade para:

1.  Fazer um **Fork** do projeto.
2.  Criar uma nova **Branch** (`git checkout -b feature/sua-feature`).
3.  Fazer o **Commit** das suas alterações (`git commit -m 'Adiciona sua-feature'`).
4.  Fazer o **Push** para a Branch (`git push origin feature/sua-feature`).
5.  Abrir um **Pull Request**.

Você também pode simplesmente abrir uma [Issue](https://github.com/seu-usuario/seu-repositorio/issues) com a tag "bug" ou "enhancement".

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
