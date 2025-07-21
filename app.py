import customtkinter as ctk
import pandas as pd
import os
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkcalendar import Calendar
from datetime import datetime

from analisador import AnalisadorClimatico
from visualizador import VisualizadorClimatico
import constantes as const

# --- Configurações Iniciais do CustomTkinter ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class AppClima(ctk.CTk):
    """
    Classe principal da aplicação. Gerencia as janelas (frames) e o estado global,
    como a instância do analisador e os dados filtrados.
    """
    def __init__(self):
        super().__init__()
        self.title("Analisador de Dados Climáticos")
        self.geometry("600x850")

        # Inicialização de variáveis de estado
        self.analisador = None
        self.current_filtered_data = None
        self.selected_start_date = None
        self.selected_end_date = None

        # Container principal para os frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Itera sobre as classes das páginas para criá-las
        for F in (StartPage, AnalysisPage, GraphOptionsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Exibe o frame especificado."""
        frame = self.frames[page_name]
        # Atualiza a descrição na página de análise sempre que ela é exibida
        if page_name == "AnalysisPage" and self.analisador:
            frame.update_description()
        frame.tkraise()

    def set_analisador(self, analisador_instance):
        self.analisador = analisador_instance

    def set_filtered_data(self, data, start_date, end_date):
        self.current_filtered_data = data
        self.selected_start_date = start_date
        self.selected_end_date = end_date

    def get_analisador(self):
        return self.analisador

    def get_filtered_data(self):
        return self.current_filtered_data

    def get_selected_period_str(self):
        start_str = self.selected_start_date.strftime('%d/%m/%Y') if self.selected_start_date else "N/A"
        end_str = self.selected_end_date.strftime('%d/%m/%Y') if self.selected_end_date else "N/A"
        return f"Período: {start_str} a {end_str}"

    def get_selected_csv_name(self):
        if self.analisador and hasattr(self.analisador, 'caminho_csv') and self.analisador.caminho_csv:
            return os.path.basename(self.analisador.caminho_csv)
        return "Nenhum arquivo carregado"

    def get_selected_style(self):
        return self.frames["StartPage"].style_combobox.get()


class GraphViewerWindow(ctk.CTkToplevel):
    """
    Janela Toplevel para exibir figuras do Matplotlib com navegação.
    """
    def __init__(self, master, figures):
        super().__init__(master)
        self.figures = figures
        self.current_figure_index = 0

        self.title("Visualizador de Gráficos")
        self.geometry("1000x700")
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.resizable(True, True)
        self.after(20, self.grab_set)

        self.fig_canvas_frame = ctk.CTkFrame(self)
        self.fig_canvas_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = None
        self.toolbar = None
        self._display_current_figure()

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(side=ctk.BOTTOM, pady=10)
        self.btn_prev = ctk.CTkButton(self.btn_frame, text="Anterior", command=self._show_prev_figure)
        self.btn_prev.pack(side=ctk.LEFT, padx=10)
        self.btn_next = ctk.CTkButton(self.btn_frame, text="Próximo", command=self._show_next_figure)
        self.btn_next.pack(side=ctk.LEFT, padx=10)

    def _apply_theme_to_figure(self, fig):
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = '#2b2b2b' if is_dark else '#f0f0f0'
        text_color = 'white' if is_dark else 'black'

        fig.patch.set_facecolor(bg_color)
        for ax in fig.get_axes():
            ax.set_facecolor("#3c3c3c" if is_dark else "#fcfcfc")
            ax.tick_params(axis='x', colors=text_color)
            ax.tick_params(axis='y', colors=text_color)
            ax.yaxis.label.set_color(text_color)
            ax.xaxis.label.set_color(text_color)
            ax.title.set_color(text_color)
            if ax.get_legend() is not None:
                plt.setp(ax.get_legend().get_texts(), color=text_color)

    def _display_current_figure(self):
        for widget in self.fig_canvas_frame.winfo_children():
            widget.destroy()

        fig_to_display = self.figures[self.current_figure_index]
        self._apply_theme_to_figure(fig_to_display)

        self.canvas = FigureCanvasTkAgg(fig_to_display, master=self.fig_canvas_frame)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.fig_canvas_frame)
        self.toolbar.update()
        self.toolbar.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    def _show_prev_figure(self):
        self.current_figure_index = (self.current_figure_index - 1) % len(self.figures)
        self._display_current_figure()

    def _show_next_figure(self):
        self.current_figure_index = (self.current_figure_index + 1) % len(self.figures)
        self._display_current_figure()

    def _on_closing(self):
        for fig in self.figures:
            plt.close(fig)
        self.destroy()


class StartPage(ctk.CTkFrame):
    """
    Página inicial da aplicação para carregar o arquivo e selecionar o período.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Analisador de Dados Climáticos", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Selecione o arquivo CSV e o período de análise", font=ctk.CTkFont(size=14)).pack(pady=(0, 20))

        self.btn_carregar = ctk.CTkButton(self, text="Carregar Arquivo CSV", command=self.carregar_csv, height=40)
        self.btn_carregar.pack(pady=10, padx=20, fill='x')

        date_frame = ctk.CTkFrame(self, fg_color="transparent")
        date_frame.pack(pady=10, padx=20, fill='x')
        date_frame.columnconfigure((0, 1), weight=1)

        start_date_frame = ctk.CTkFrame(date_frame)
        start_date_frame.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        ctk.CTkLabel(start_date_frame, text="Data Início:").pack(pady=5)
        self.data_inicio_entry = ctk.CTkEntry(start_date_frame, placeholder_text="AAAA-MM-DD")
        self.data_inicio_entry.pack(side=ctk.LEFT, expand=True, fill='x', padx=5, pady=5)
        ctk.CTkButton(start_date_frame, text="🗓", width=30, command=lambda: self._show_calendar_popup(self.data_inicio_entry)).pack(side=ctk.RIGHT, padx=(0, 5), pady=5)

        end_date_frame = ctk.CTkFrame(date_frame)
        end_date_frame.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        ctk.CTkLabel(end_date_frame, text="Data Fim:").pack(pady=5)
        self.data_fim_entry = ctk.CTkEntry(end_date_frame, placeholder_text="AAAA-MM-DD")
        self.data_fim_entry.pack(side=ctk.LEFT, expand=True, fill='x', padx=5, pady=5)
        ctk.CTkButton(end_date_frame, text="🗓", width=30, command=lambda: self._show_calendar_popup(self.data_fim_entry)).pack(side=ctk.RIGHT, padx=(0, 5), pady=5)

        ctk.CTkLabel(self, text="Estilo do Gráfico:").pack(pady=(10, 5))
        self.style_combobox = ctk.CTkComboBox(self, state="readonly", values=['whitegrid', 'darkgrid', 'dark', 'white', 'ticks', 'pastel', 'muted'])
        self.style_combobox.set('darkgrid')
        self.style_combobox.pack(pady=(0, 20))

        self.btn_avancar = ctk.CTkButton(self, text="Analisar Dados", command=self.avancar_para_analise, height=40, state="disabled")
        self.btn_avancar.pack(pady=20, padx=20, fill='x')

    def _show_calendar_popup(self, target_entry):
        if not self.controller.analisador:
            messagebox.showwarning("Atenção", "Carregue um arquivo CSV primeiro.")
            return

        calendar_top = ctk.CTkToplevel(self)
        calendar_top.title("Selecionar Data")
        calendar_top.transient(self.controller)
        calendar_top.after(20, calendar_top.grab_set)

        dados = self.controller.analisador.get_dados_completos()
        min_date, max_date = (None, None)
        if not dados.empty:
            min_date = dados['data'].min().date()
            max_date = dados['data'].max().date()

        cal = Calendar(calendar_top, selectmode='day', date_pattern='yyyy-mm-dd', mindate=min_date, maxdate=max_date)
        cal.pack(pady=20, padx=20)

        def set_date_and_close():
            target_entry.delete(0, ctk.END)
            target_entry.insert(0, cal.get_date())
            calendar_top.destroy()

        ctk.CTkButton(calendar_top, text="Selecionar", command=set_date_and_close).pack(pady=10)

    def carregar_csv(self):
        caminho = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not caminho:
            return
        try:
            analisador = AnalisadorClimatico(caminho)
            self.controller.set_analisador(analisador)
            messagebox.showinfo("Sucesso", f"Arquivo '{os.path.basename(caminho)}' carregado.")
            dados = analisador.get_dados_completos()
            if not dados.empty:
                self.data_inicio_entry.delete(0, ctk.END)
                self.data_inicio_entry.insert(0, dados['data'].min().strftime('%Y-%m-%d'))
                self.data_fim_entry.delete(0, ctk.END)
                self.data_fim_entry.insert(0, dados['data'].max().strftime('%Y-%m-%d'))
                self.btn_avancar.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", f"Não foi possível carregar ou processar o arquivo.\nVerifique o formato das colunas.\n\nErro: {e}")
            self.controller.set_analisador(None)
            self.btn_avancar.configure(state="disabled")

    def avancar_para_analise(self):
        data_inicio_str = self.data_inicio_entry.get()
        data_fim_str = self.data_fim_entry.get()

        if not data_inicio_str or not data_fim_str:
            messagebox.showwarning("Datas em Falta", "Por favor, preencha as datas de início e fim.")
            return
        try:
            data_inicio = pd.to_datetime(data_inicio_str)
            data_fim = pd.to_datetime(data_fim_str)
        except ValueError:
            messagebox.showerror("Formato Inválido", "Formato de data inválido. Use AAAA-MM-DD.")
            return

        if data_inicio > data_fim:
            messagebox.showwarning("Período Inválido", "A data de início não pode ser posterior à data de fim.")
            return

        dados_filtrados = self.controller.analisador.get_dados_filtrados_para_plot(data_inicio, data_fim)
        if dados_filtrados.empty:
            messagebox.showinfo("Sem Dados", "Nenhum dado encontrado para o período selecionado.")
            return

        self.controller.set_filtered_data(dados_filtrados, data_inicio, data_fim)
        self.controller.show_frame("AnalysisPage")


class AnalysisPage(ctk.CTkFrame):
    """
    Página principal de análise, exibe resumos e oferece opções de visualização.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.csv_info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.csv_info_label.pack(pady=(5,0))
        self.period_info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=14))
        self.period_info_label.pack()
        self.style_info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=14))
        self.style_info_label.pack(pady=(0,5))

        self.btn_mostrar_dados = ctk.CTkButton(self, text="Exibir Tabela de Dados do Período", command=self.mostrar_todos_dados)
        self.btn_mostrar_dados.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        botoes_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        botoes_frame.columnconfigure((0, 1), weight=1)
        self.btn_estatisticas = ctk.CTkButton(botoes_frame, text="Visualizar Estatísticas", command=self.mostrar_estatisticas)
        self.btn_estatisticas.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.btn_opcoes_grafico = ctk.CTkButton(botoes_frame, text="Mais Opções de Gráficos", command=lambda: self.controller.show_frame("GraphOptionsPage"))
        self.btn_opcoes_grafico.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="ew")

        self.btn_gerar_resumo = ctk.CTkButton(self, text="Gerar Resumo Inteligente", command=self.gerar_resumo)
        self.btn_gerar_resumo.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.resumo_textbox = ctk.CTkTextbox(self, wrap="word", font=("Segoe UI", 13), state="disabled")
        self.resumo_textbox.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        botoes_finais_frame = ctk.CTkFrame(self, fg_color="transparent")
        botoes_finais_frame.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
        botoes_finais_frame.columnconfigure((0, 1), weight=1)
        self.btn_voltar = ctk.CTkButton(botoes_finais_frame, text="Mudar Período", fg_color="gray50", hover_color="gray30", command=lambda: self.controller.show_frame("StartPage"))
        self.btn_voltar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.btn_exportar = ctk.CTkButton(botoes_finais_frame, text="Novo Recorte dos Dados para CSV", command=self.exportar_csv)
        self.btn_exportar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def update_description(self):
        self.csv_info_label.configure(text=self.controller.get_selected_csv_name())
        self.period_info_label.configure(text=self.controller.get_selected_period_str())
        self.style_info_label.configure(text=f"Estilo de Gráfico: {self.controller.get_selected_style()}")
        self.resumo_textbox.configure(state="normal")
        self.resumo_textbox.delete("1.0", "end")
        self.resumo_textbox.insert("1.0", "Clique em 'Gerar Resumo Inteligente' para uma análise comparativa do período.")
        self.resumo_textbox.configure(state="disabled")

    def mostrar_estatisticas(self):
        """Gera e exibe o dashboard híbrido de estatísticas."""
        analisador = self.controller.get_analisador()
        estatisticas, _ = analisador.gerar_estatisticas(
            self.controller.selected_start_date, self.controller.selected_end_date
        )
        if not estatisticas:
            messagebox.showinfo("Sem Dados", "Nenhum dado disponível para gerar estatísticas.")
            return
        visualizador = VisualizadorClimatico(None)
        fig = visualizador.plotar_dashboard_hibrido(estatisticas)
        if fig:
            GraphViewerWindow(self.controller, [fig])

    def gerar_resumo(self):
        analisador = self.controller.get_analisador()
        resumo = analisador.gerar_resumo_inteligente(self.controller.selected_start_date, self.controller.selected_end_date)
        self.resumo_textbox.configure(state="normal")
        self.resumo_textbox.delete("1.0", "end")
        self.resumo_textbox.insert("1.0", resumo)
        self.resumo_textbox.configure(state="disabled")

    def exportar_csv(self):
        dados_filtrados = self.controller.get_filtered_data()
        if dados_filtrados is None or dados_filtrados.empty:
            messagebox.showinfo("Sem Dados", "Não há dados para exportar.")
            return
        initial_filename = f"dados_filtrados_{self.controller.selected_start_date.strftime('%Y%m%d')}_{self.controller.selected_end_date.strftime('%Y%m%d')}.csv"
        filepath = filedialog.asksaveasfilename(
            initialfile=initial_filename,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            dados_filtrados.to_csv(filepath, index=False)
            messagebox.showinfo("Sucesso", f"Dados exportados com sucesso para:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Erro ao Exportar", f"Não foi possível guardar o arquivo.\n\nErro: {e}")

    def mostrar_todos_dados(self):
        """Exibe os dados brutos do período selecionado em uma nova janela."""
        dados = self.controller.get_filtered_data()
        if dados is None or dados.empty:
            messagebox.showinfo("Sem Dados", "Nenhum dado para exibir.")
            return
        top = ctk.CTkToplevel(self)
        top.title("Tabela de Dados do Período")
        top.geometry("850x500")
        top.transient(self.controller)
        top.after(20, top.grab_set)
        text_widget = ctk.CTkTextbox(top, font=("monospace", 10), wrap="none", text_color=("gray10", "#DCE4EE"))
        text_widget.pack(padx=10, pady=10, fill="both", expand=True)
        try:
            dados_str = dados.to_markdown(index=False)
        except ImportError:
            pd.options.display.float_format = '{:,.2f}'.format
            dados_str = dados.to_string(index=False)
        text_widget.insert("1.0", dados_str)
        text_widget.configure(state="disabled")


class GraphOptionsPage(ctk.CTkFrame):
    """
    Página com opções avançadas de gráficos.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Opções Avançadas de Gráfico", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        sazonal_frame = ctk.CTkFrame(self)
        sazonal_frame.pack(pady=5, padx=20, fill='x')
        ctk.CTkLabel(sazonal_frame, text="Análise Sazonal (Período Selecionado)", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        ctk.CTkButton(sazonal_frame, text="Gerar Gráfico de Análise Mensal", command=self.gerar_grafico_mensal).pack(pady=5, fill='x')

        extremos_frame = ctk.CTkFrame(self)
        extremos_frame.pack(pady=5, padx=20, fill='x')
        ctk.CTkLabel(extremos_frame, text="Análise de Dias Extremos (Dados Gerais)", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.metricas_map = {
            "Temperatura": (const.COL_TEMP, "°C", "YlOrRd", "Blues_r"),
            "Umidade": (const.COL_UMIDADE, "%", "Greens", "GnBu_r"),
            "Vento": (const.COL_VENTO, " km/h", "Oranges", "Purples_r"),
            "Precipitação": (const.COL_PRECIP, " mm", "Blues", "Reds_r")
        }
        self.metrica_selecionada = ctk.StringVar(value="Temperatura")
        self.tipo_extremo_selecionado = ctk.StringVar(value="Maiores Índices")
        ctk.CTkLabel(extremos_frame, text="Selecione a Métrica:").pack()
        ctk.CTkComboBox(extremos_frame, variable=self.metrica_selecionada, values=list(self.metricas_map.keys())).pack(pady=5)
        ctk.CTkLabel(extremos_frame, text="Selecione o Tipo de Extremo:").pack()
        ctk.CTkSegmentedButton(extremos_frame, variable=self.tipo_extremo_selecionado, values=["Maiores Índices", "Menores Índices"]).pack(pady=5)
        ctk.CTkButton(extremos_frame, text="Gerar Gráfico de Extremos", command=self.gerar_grafico_extremos).pack(pady=(10,5), fill='x')

        geral_frame = ctk.CTkFrame(self)
        geral_frame.pack(pady=10, padx=20, fill='x')
        ctk.CTkLabel(geral_frame, text="Análise Geral e Estatística (Dados Gerais)", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        ctk.CTkButton(geral_frame, text="Gerar Heatmap de Correlação", command=self.gerar_heatmap).pack(pady=5, fill='x')
        ctk.CTkButton(geral_frame, text="Gerar Histograma de Temperatura", command=self.gerar_histograma_temperatura).pack(pady=5, fill='x')
        ctk.CTkButton(geral_frame, text="Visualizar Gráficos Principais do Período", command=self.visualizar_graficos_periodo).pack(pady=5, fill='x')

        self.btn_voltar = ctk.CTkButton(self, text="Voltar para Análise", height=40, command=lambda: self.controller.show_frame("AnalysisPage"))
        self.btn_voltar.pack(pady=20, padx=20, fill='x', side='bottom')

    def gerar_grafico_mensal(self):
        analisador = self.controller.get_analisador()
        dados_mensais = analisador.gerar_analise_mensal(self.controller.selected_start_date, self.controller.selected_end_date)
        if dados_mensais.empty:
            messagebox.showinfo("Sem Dados", "Não há dados suficientes no período para a análise mensal.")
            return
        visualizador = VisualizadorClimatico(dados_mensais)
        fig = visualizador.plotar_analise_mensal(dados_mensais)
        if fig:
            GraphViewerWindow(self.controller, [fig])

    def gerar_grafico_extremos(self):
        analisador = self.controller.get_analisador()
        if not analisador:
            messagebox.showwarning("Atenção", "Nenhum arquivo CSV carregado.")
            return
        metrica_nome = self.metrica_selecionada.get()
        tipo_extremo = self.tipo_extremo_selecionado.get()
        coluna, unidade, paleta_maior, paleta_menor = self.metricas_map[metrica_nome]
        titulo = f"Top 5 Dias com {tipo_extremo} de {metrica_nome}"
        if tipo_extremo == "Maiores Índices":
            df_extremos = analisador.buscar_maiores_indices(coluna)
            paleta = paleta_maior
        else:
            df_extremos = analisador.buscar_menores_indices(coluna)
            paleta = paleta_menor
        if df_extremos.empty:
            messagebox.showinfo("Sem Dados", f"Não foi possível encontrar dados para os extremos de {metrica_nome}.")
            return
        visualizador = VisualizadorClimatico(df_extremos)
        fig = visualizador.plotar_dias_extremos(df_extremos, coluna, titulo, paleta, unidade)
        if fig:
            GraphViewerWindow(self.controller, [fig])

    def gerar_heatmap(self):
        analisador = self.controller.get_analisador()
        if not analisador:
            messagebox.showwarning("Atenção", "Nenhum arquivo CSV carregado.")
            return
        matriz_corr = analisador.gerar_matriz_correlacao()
        visualizador = VisualizadorClimatico(None)
        fig = visualizador.plotar_heatmap_correlacao(matriz_corr)
        if fig:
            GraphViewerWindow(self.controller, [fig])

    def gerar_histograma_temperatura(self):
        analisador = self.controller.get_analisador()
        if not analisador:
            messagebox.showwarning("Atenção", "Nenhum arquivo .CSV carregado.")
            return
        dados_completos = analisador.get_dados_completos()
        visualizador = VisualizadorClimatico(dados_completos)
        fig = visualizador.plotar_distribuicao(const.COL_TEMP, 'Temperatura')
        if fig:
            GraphViewerWindow(self.controller, [fig])

    def visualizar_graficos_periodo(self):
        dados_filtrados = self.controller.get_filtered_data()
        if dados_filtrados is None or dados_filtrados.empty:
            messagebox.showinfo("Sem Dados", "Não há dados no período selecionado.")
            return
        visualizador = VisualizadorClimatico(dados_filtrados)
        figures = visualizador.plotar_graficos()
        if figures:
            GraphViewerWindow(self.controller, figures)


# --- Bloco Principal ---
if __name__ == "__main__":
    app = AppClima()
    app.mainloop()