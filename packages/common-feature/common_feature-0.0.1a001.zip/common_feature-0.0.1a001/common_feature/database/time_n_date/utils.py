# -*- coding: utf-8 -*-

import datetime


class Date(object):

    @staticmethod
    def day_month_format(day_month):
        try:
            day_month = int(day_month)
        except:
            return '0'
        return '0'+str(day_month) if len(str(day_month)) == 1 else str(day_month)

    @staticmethod
    def get_day(year, month):
        import calendar
        days = [31, 29 if calendar.isleap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month-1]

    @staticmethod
    def get_day_with_month(month):
        days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month-1]

    @staticmethod
    def _dayscoount(date, duration_month):
        days = 0
        count = 0
        year = date.year
        for x in range(1, duration_month+1):
            next_month = (date.month + x) - (12*count)
            if next_month >= 12:
                year += 1
                count += 1
            flag, day, msg = Date.get_day(year, next_month)
            days += day
        return days

    @staticmethod
    def _get_start_date_end_date_default(start_date=None, end_date=None):
        today = datetime.date.today
        if start_date is None and end_date is None:
            start_date = datetime.datetime(year=today().year, month=today().month, day=1)
            flag, day, msg = Date.get_day(year=today().year, month=today().month)
            end_date = datetime.datetime(
                year=today().year,
                month=today().month,
                day=day,
            )
        return True, [start_date, end_date], ""


    @staticmethod
    def get_days_in_month_without(start_date, end_date, exclude_day=[6], with_holiday=False, province=None,):
        if max(exclude_day) >= 7 or min(exclude_day) < 0:
            return False, "", "must be range of (0(monday), 6(sunday))"
        count_days = (end_date - start_date).days + 1
        total_count = count_days
        for i in range(total_count+1):
            for j in exclude_day:
                exclusion = (start_date+datetime.timedelta(i)).weekday() == j
                if with_holiday:
                    #holiday = HolidayUtils.get_hollday(date=start_date+datetime.timedelta(i))
                    holiday = None
                    if exclusion or holiday:
                        count_days -= 1
                else:
                    if exclusion:
                        count_days -= 1

        return count_days

    @staticmethod
    def get_date_range(data=None):
        """
        data = {
            'day': utils.day_month_format(day),
            'month': utils.day_month_format(month),
            'year': year,
            'days': days,
            'day1': utils.day_month_format(day1),
            'month1': utils.day_month_format(month1),
            'year1': year1,
            'months': months,
            'years': years,
            'chkEndDate': False if not self.request.GET.get('chkEndDate') else True,
            'rdoType': rdoType,
        }
        """
        today = datetime.datetime.today()
        if not data:
            start_date = datetime.datetime(day=today.day, month=today.month, year=today.year, hour=0, minute=0, second=0)
            end_date = datetime.datetime(day=today.day, month=today.month, year=today.year, hour=today.hour, minute=today.minute, second=today.second)
            return start_date, end_date
        if data['rdoType'] == '2':
            if data['chkEndDate']:
                start_date = datetime.datetime(day=int(data['day']), month=int(data['month']), year=int(data['year']), hour=0, minute=0, second=0)
                end_date = datetime.datetime(day=int(data['day']), month=int(data['month']), year=int(data['year']), hour=23, minute=59, second=59)
            else:
                start_date = datetime.datetime(day=int(data['day']), month=int(data['month']), year=int(data['year']), hour=0, minute=0, second=0)
                end_date = datetime.datetime(day=int(data['day1']), month=int(data['month1']), year=int(data['year1']), hour=23, minute=59, second=59)
        elif data['rdoType'] == '3':
            start_date = datetime.datetime(day=1, month=3, year=2016, hour=0, minute=0, second=0)
            end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
        elif data['rdoType'] == '5':
            if data['days'] != '0':
                start_day = datetime.datetime.today() - datetime.timedelta(days=int(data['days']))
                if data['days'] == '1':
                    start_date = datetime.datetime(year=start_day.year, month=start_day.month, day=start_day.day, hour=0, minute=0, second=0)
                    end_date = datetime.datetime(year=start_day.year, month=start_day.month, day=start_day.day, hour=23, minute=59, second=59)
                else:
                    start_date = datetime.datetime(year=start_day.year, month=start_day.month, day=start_day.day, hour=0, minute=0, second=0)
                    end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
            else:
                start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
                end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)
        elif data['rdoType'] == '6':
            start_date = datetime.datetime(year=today.year, month=int(data['months']), day=1, hour=0, minute=0, second=0)
            end_date = datetime.datetime(year=today.year, month=int(data['months']), day=_utils.get_day(year=today.year, month=int(data['months'])), hour=23, minute=59, second=59)
        elif data['rdoType'] == '7':
            start_date = datetime.datetime(year=int(data['years']), month=1, day=1, hour=0, minute=0, second=0)
            end_date = datetime.datetime(year=int(data['years']), month=12, day=31, hour=23, minute=59, second=59)
        else:
            start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
            end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59, second=59)

        return start_date, end_date


class Time(object):
    @staticmethod
    def time_operation(start_time, end_time):
        diff = datetime.datetime.combine(datetime.datetime.now(), end_time) - datetime.datetime.combine(datetime.datetime.now(), start_time)
        d = str(diff).split(':')
        return datetime.time(int(d[0]), int(d[1]), int(d[2]))