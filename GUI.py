import tkinter as tk
from tkinter import ttk, messagebox
from databaseConnection import database_connection
from datetime import datetime
import re

class RestauranteDaCamilaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas - Restaurante da Camila")

        # Variáveis para armazenar os dados das reservas
        self.reservas = {}

        # Criar os widgets
        self.label_nome = ttk.Label(root, text="Nome:")
        self.entry_nome = ttk.Entry(root)
        self.label_telefone = ttk.Label(root, text="Telefone:")
        self.entry_telefone = ttk.Entry(root)
        self.label_email = ttk.Label(root, text="E-mail:")
        self.entry_email = ttk.Entry(root)
        self.label_data = ttk.Label(root, text="Data:")
        self.entry_data = ttk.Entry(root)
        self.label_mesa = ttk.Label(root, text="Mesa:")
        self.entry_mesa = ttk.Entry(root)
        self.label_horario = ttk.Label(root, text="Horário:")
        self.entry_horario = ttk.Entry(root)
        self.btn_reservar = ttk.Button(root, text="Fazer Reserva", command=self.fazer_reserva)
        
        self.btn_visualizar_reservas = ttk.Button(root, text="Visualizar Reservas", command=self.visualizar_reservas)

        # Posicionar os widgets na janela
        self.label_nome.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=5)
        self.label_telefone.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_telefone.grid(row=1, column=1, padx=10, pady=5)
        self.label_email.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)
        self.label_data.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entry_data.grid(row=3, column=1, padx=10, pady=5)
        self.label_mesa.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_mesa.grid(row=4, column=1, padx=10, pady=5)
        self.label_horario.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entry_horario.grid(row=5, column=1, padx=10, pady=5)
        self.btn_reservar.grid(row=6, column=0, columnspan=2, pady=10)
        self.btn_visualizar_reservas.grid(row=7, column=0, columnspan=2, pady=5)

    def fazer_reserva(self):
        nome = self.obtem_nome()
        telefone = self.obtem_telefone()
        data = self.obtem_data_reserva()
        mesa = self.entry_mesa.get()
        horario = self.entry_horario.get()

        if nome and telefone and data and mesa and horario:
            if data not in self.reservas:
                self.reservas[data] = {}
            if mesa not in self.reservas[data]:
                self.reservas[data][mesa] = {}
            if horario not in self.reservas[data][mesa]:
                self.reservas[data][mesa][horario] = {"Nome": nome, "Telefone": telefone}
                self.btn_reservar = ttk.Button(self.root, text="Fazer Reserva", command=self.insere_base_dados())
                messagebox.showinfo("Reserva Efetuada", "Reserva feita com sucesso!")
            else:
                messagebox.showerror("Erro", "Este horário nesta mesa já está reservado.")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def visualizar_reservas(self):
        if not self.reservas:
            messagebox.showinfo("Reservas", "Não há reservas cadastradas.")
        else:
            visualizacao = ""
            for data, mesas in self.reservas.items():
                visualizacao += f"Data: {data}\n"
                for mesa, horarios in mesas.items():
                    visualizacao += f" - Mesa: {mesa}\n"
                    for horario, reserva in horarios.items():
                        visualizacao += f"    - Horário: {horario}, Nome: {reserva['Nome']}, Telefone: {reserva['Telefone']}\n"
                visualizacao += "\n"
            messagebox.showinfo("Reservas", visualizacao)



    def remover_caracteres_especiais(self, texto):
        padrao = re.compile(r'[^a-zA-Z0-9\s]') # Remove tudo exceto letras, números e espaços
        texto_limpo = re.sub(padrao, '', texto)
        return texto_limpo

    def obtem_nome(self):
        nome_reserva = self.entry_nome.get()
        if nome_reserva.strip():  # Verifica se o nome não está vazio ou contém apenas espaços em branco
            return nome_reserva
        else:
            messagebox.showerror('Erro', 'Nome inválido!')

    def obtem_data_reserva(self):
        dt_reserva = self.entry_data.get()
        dt_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        try:
            dt_reserva_obj = datetime.strptime(dt_reserva, '%d/%m/%Y').replace(hour=0, minute=0, second=0, microsecond=0)
            if dt_reserva_obj >= dt_atual:
                return dt_reserva_obj.strftime('%d/%m/%Y')
            else:
                messagebox.showerror('Erro', 'A data inserida é menor do que a atual!')
        except ValueError:
            messagebox.showerror('Erro', 'Informe uma data válida!')

    def obtem_telefone(self):
        telefone = self.entry_telefone.get()
        telefone_limpo = self.remover_caracteres_especiais(telefone)
        if len(telefone_limpo) >= 9 and len(telefone_limpo) <= 12:
            return telefone_limpo
        else:
            messagebox.showerror('Erro', 'Informe um telefone válido!')

        
          
    def insere_base_dados(self):
        cursor, connection = database_connection()
        if cursor and connection:
            cursor.execute('INSERT INTO REGISTRO_RESERVA(NOME_RESERVA, DATA_RESERVA, HORARIO_RESERVA, TELEFONE, EMAIL, MESA_RESERVADA) VALUES (?,?,?,?,?,?)', (self.obtem_nome(), self.obtem_data_reserva(), self.entry_horario.get(), self.obtem_telefone(), self.valida_email(), self.entry_mesa.get()))
            
            connection.commit()
            connection.close()
        else:
            tk.messagebox.showerror("Erro", "Não foi possível estabelecer a conexão com o banco de dados")


    def valida_email(self):
        email = self.entry_email.get()
        regex = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
        if re.match(regex, email):
            return email
        else:
            messagebox.showerror('Informe um e-mail válido!')

def main():
    root = tk.Tk()
    app = RestauranteDaCamilaApp(root)
    root.mainloop()
 

if __name__ == "__main__":
    main()