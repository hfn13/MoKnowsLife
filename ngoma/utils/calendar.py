from calendar import HTMLCalendar
from datetime import date

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, events):
        super().__init__()
        self.events = events
        self.year = None
        self.month = None

    def formatmonth(self, year, month):
        self.year = year
        self.month = month
        html = super().formatmonth(year, month)
        return f'<div class="calendar-wrapper">{html}</div>'

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        day_date = date(self.year, self.month, day).isoformat()
        day_events = self.events.get(day_date, [])

        # Build event dots
        dots_html = ""
        if day_events:
            dots_html = '<div class="event-dots">'
            for _ in day_events:
                dots_html += '<span class="event-dot"></span>'
            dots_html += '</div>'

        return f'''
            <td class="day" data-date="{day_date}">
                <div class="date-number">{day}</div>
                {dots_html}
            </td>
        '''
