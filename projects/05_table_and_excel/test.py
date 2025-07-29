from openpyxl import Workbook # type: ignore

wb = Workbook()
ws = wb.active
ws.append(["ID", "Name", "Age"])
ws.append([1, "Andres", 21])
wb.save("test.xlsx")