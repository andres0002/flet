# py
import io
import base64
from datetime import datetime, timedelta
# flet
import flet as ft # type: ignore
# third
import yfinance as yf # type: ignore
from matplotlib.figure import Figure
# owm

def main(page: ft.Page):
    page.title = "Flet with Pandas and Matplotlib"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.on_scroll = None
    
    def create_dlg_modal(title, description):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, text_align=ft.TextAlign.CENTER),
            content=ft.Text(description),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        return dlg_modal
    
    title = ft.Text("Flet with Pandas and Matplotlib", size=30, weight="bold")
    
    divider = ft.Divider()
    
    # control deslizante
    def on_zoom_change(event):
        zoom_level = event.control.value
        content.scale = zoom_level
        zoom_text.value = f"Zoom: {zoom_level:.2f}x"
        page.update()
    
    # text para mostrar el nivel del zoom current
    zoom_text = ft.Text("Zoom: 0.80x", size=14)
    
    # slider para controlar el zoom
    zoom_slider = ft.Slider(
        min=0.5,
        max=2.0,
        value=0.8,
        divisions=15,
        label="Zoom",
        on_change=on_zoom_change,
        width=200
    )
    
    # function para get data de acciones
    def get_stock_data(symbol, period="1mo"):
        end_data = datetime.now()
        start_date = end_data - timedelta(days=30)
        df = yf.download(symbol, start=start_date, end=end_data)
        return df
    
    # function para create gráfico
    def create_stock_chart(symbol):
        df = get_stock_data(symbol)
        fig = Figure(figsize=(10, 6), facecolor="none")
        ax = fig.add_subplot(111)
        ax.set_facecolor("none")
        smoothed_data = df["Close"].rolling(window=2, min_periods=1).mean()
        ax.plot(df.index, smoothed_data, color="#1E88E5", linewidth=2.5, alpha=0.9)
        ax.set_title(f"Precio de cierre para {symbol}", color="#ffffff")
        ax.set_xlabel("Fecha", color="#ffffff")
        ax.set_ylabel("Precio (USD)", color="#ffffff")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.tick_params(colors="#ffffff")
        fig.autofmt_xdate()
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    
    # controls interface
    def update_chart(_):
        symbol = input_symbol.value
        try:
            chart_bytes = create_stock_chart(symbol)
            image_stock.src_base64 = chart_bytes
            page.update()
        except Exception as _:
            dlg_modal = create_dlg_modal(
                "Error",
                f"No se pudierón obtener datos para {symbol}."
            )
            page.open(dlg_modal)
    
    input_symbol = ft.Dropdown(
        label="Símbolo de la acción",
        options=[
            ft.DropdownOption(
                key="AAPL",
                content=ft.Text(
                    "AAPL",
                ),
            ),
            ft.DropdownOption(
                key="NVDA",
                content=ft.Text(
                    "NVDA",
                ),
            ),
            ft.DropdownOption(
                key="MSFT",
                content=ft.Text(
                    "MSFT",
                ),
            ),
            ft.DropdownOption(
                key="GOOGL",
                content=ft.Text(
                    "GOOGL",
                ),
            ),
            ft.DropdownOption(
                key="TSLA",
                content=ft.Text(
                    "TSLA",
                ),
            )
        ],
        value="AAPL",
        width=400
    )
    image_stock = ft.Image(fit=ft.ImageFit.CONTAIN)
    
    btn_update = ft.ElevatedButton(
        text="Update Graphic",
        on_click=update_chart
    )
    
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Explorador de datos de acciones", size=20, weight="bold"),
                input_symbol,
                btn_update,
                zoom_text,
                zoom_slider,
                image_stock
            ],
            expand=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        ),
        expand=1,
        scale=1
    )
    
    update_chart(None)
    
    page.add(
        title,
        divider,
        content,
        divider
    )

ft.app(target=main)