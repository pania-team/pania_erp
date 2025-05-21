from datetime import date

def daily_message(request):
    messages = [
        "سلام بر تو و بر زلف عنبر افشانت",
        "طلوع امروز را با لبخندت آغاز کن",
        "دلت شاد، چشمت روشن، روزت پُر از امید",
        "امروز هم یکی از فرصت‌های ناب زندگی است",
        "لبخند بزن، زندگی در جریان است",
        "صبح نزدیک است , امیدوار باش",
        "هر طلوع، فرصتی دوباره برای درخشیدن است.",
    ]
    index = date.today().toordinal() % len(messages)
    return {'daily_message': messages[index]}
