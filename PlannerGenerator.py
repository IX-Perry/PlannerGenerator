from datetime import datetime, timedelta
from fpdf import FPDF
import calendar
from pathlib import Path

def getDate(Prompt):
    while True:
        dateStr = input(Prompt + " (DD-MM-YYYY): ")
        try:
            validDate = datetime.strptime(dateStr, "%d-%m-%Y").date()
            return validDate
        except ValueError:
            print("Please use the DD-MM-YYYY format (e.g., 27-07-2026).\n")


def calendarGen(x, y, date):
    pdf.set_font_size(12)
    pdf.text(x + 1, y - 2, str(calendar.month_name[date.month]))

    pdf.set_font_size(8)
    pdf.set_line_width(0.2)

    pdf.text(x + 0 + 1, y + 3, "M")
    pdf.text(x + 5 + 1, y + 3, "T")
    pdf.text(x + 10 + 1, y + 3, "W")
    pdf.text(x + 15 + 1, y + 3, "T")
    pdf.text(x + 20 + 1, y + 3, "F")
    pdf.text(x + 25 + 1, y + 3, "S")
    pdf.text(x + 30 + 1, y + 3, "S")

    monthDate = datetime.strptime("01-" + str(date.month) +"-"+ str(date.year), "%d-%m-%Y").date() #gets first of month
    monthStartDay = calendar.weekday(monthDate.year, monthDate.month, monthDate.day)

    cell = 0
    for i in range(0,42):
        line = cell // 7
        xSpacing = cell%7 * 5
        ySpacing = line * 4 + 8
        if cell < monthStartDay or monthDate.month != date.month:
            pdf.text(x + xSpacing + 1, y + ySpacing, " -")
        else:
            pdf.text(x + xSpacing + 1, y + ySpacing, str(monthDate.day))
            monthDate = monthDate + timedelta(days=1)
        cell += 1

    for i in range(1, 7):
        spacing = i * 5
        pdf.line(x + spacing, y, x + spacing, y + 28)

#startup get info
startDate = getDate("Enter start date")
endDate = getDate("Enter end date")
daysPerPage = int(input("Days per page: "))
#startup do calculations
startYear = startDate.year
daysToGenerate = endDate - startDate

#pdf setup
pdf = FPDF(orientation='P', unit='mm', format='A5')
pdf.set_auto_page_break(auto=True, margin=15)

l = 0
while l < daysToGenerate.days:

    pdf.add_page()
    pdf.set_font('Arial', 'B', size=24)
    date = startDate + timedelta(days=l)

    monthName = calendar.month_name[date.month]
    title = monthName + "   " + str(date.year)
    pdf.cell(0,20, title, ln=True, align='L')

    #formatting lines
    pdf.set_line_width(1.2)
    pdf.line(10,25,138,25) #top line
    pdf.line(10, 165, 138, 165) #bottom line
    pdf.line(53, 175, 53, 195) #left calendar split
    pdf.line(95, 175, 95, 195) #right calendar split

    dayHeight = 140 / daysPerPage
    for i in range(0, daysPerPage): #drawing days
        pdf.set_line_width(0.8)
        pdf.dashed_line(14, 25 + i*dayHeight, 134, 25 + i*dayHeight, 8, 8.1) #day separators
        dayNum = i*dayHeight
        date = startDate + timedelta(days=l)
        dateName = calendar.day_abbr[calendar.weekday(date.year, date.month, date.day)] +" "+ str(date.day) +" "+ calendar.month_abbr[date.month]
        pdf.set_font_size(12)
        pdf.text(15, dayNum + 30, dateName) #day title
        liney = dayNum + 30
        pdf.set_line_width(0.2)
        while liney < dayNum + dayHeight + 20: #day lines
            liney += 5
            pdf.dashed_line(15, liney, 138, liney, 0.1, 0.3)
        l+=1

    calendarGen(57.5, 172, date)
    firstOfMonth = datetime.strptime("01-" + str(date.month) +"-"+ str(date.year), "%d-%m-%Y").date()
    prevMonth = firstOfMonth - timedelta(days=1)
    calendarGen(10, 172, prevMonth)
    nextMonth = firstOfMonth + timedelta(days=32)
    calendarGen(100, 172, nextMonth)

desktopPath = Path.cwd().parent
filename = f"Planner_{startDate.strftime('%d-%m-%Y')}.pdf"
savePath = desktopPath / filename
print(savePath)
pdf.output(str(savePath))

close = input(" ")

#test