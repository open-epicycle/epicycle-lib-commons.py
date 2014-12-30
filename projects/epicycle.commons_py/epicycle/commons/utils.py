import time
import unicodedata

def get_domain(url):
    return '/'.join(url.split('/')[:3])

def format_time_span(secs):
    if secs < 1.:
        return "%dms" % round(secs * 1000)
    elif secs < 60.:
        return "%.1fs" % secs
    else:
        time_int = int(round(secs))
        
        secs_part = time_int % 60
        time_int /= 60
        mins_part = time_int % 60
        time_int /= 60
        hours_part = time_int % 24
        time_int /= 24
        days_part = time_int

        result = "%02d:%02d" % (mins_part, secs_part)
        
        if days_part != 0:
            result = ("%dd %02d:" % (days_part, hours_part)) + result
        elif hours_part != 0:
            result = ("%02d:" % hours_part) + result
        
        return result

def unicode_to_ascii(ustr):
    return unicodedata.normalize('NFKD', ustr).encode('ascii', 'replace')
        
def render_progress_bar(progress, char_full="*", char_empty=".", prefix="[", postfix="]", width=20):
    full_chars = int(round(width * progress))
    return prefix + (char_full * full_chars) + (char_empty * (width - full_chars)) + postfix
        
def render_percentage(x):
    return ("%02d%% " % (int(x * 100))).ljust(5)
        
class Progress(object):
    def __init__(self, steps):
        self._steps = steps
        self._progress = 0
        
    def start(self):
        self._start_time = time.clock()
        
    def increase(self):
        self._progress += 1
    
    def report(self):
        est_str = ""
        if self._progress > 0:
            secs_passed = time.clock() - self._start_time
            est_time = (secs_passed / self._progress) * self._steps
            rem_time = (est_time - secs_passed)
            
            est_str = " R: " + format_time_span(rem_time) + " E: " + format_time_span(secs_passed) + " T: " + format_time_span(est_time)
    
        progress = float(self._progress) / self._steps
        
        progress_str = ""
        progress_str += "[%d/%d] " % (self._progress, self._steps)
        progress_str += render_percentage(progress)
        progress_str += render_progress_bar(progress)
        progress_str += est_str
        
        return progress_str

class HistogramReporter(object):
    def __init__(self, prefix, config):
        self._prefix = prefix
        self._config = config
        self._total_count = 0
        self._counts = {}
        for c in config:
            self._counts[c[0]] = 0
        
    def increase(self, item):
        self._total_count += 1
        self._counts[item] += 1
        
    def report(self):
        items = []
        max_count = max([self._counts[x[0]] for x in self._config])

        if self._total_count > 0:
            for c in self._config:
                item = {}
                item['label'] = c[1]
                item['count'] = self._counts[c[0]]
                count = float(item['count'])
                item['portion'] = count / self._total_count
                item['norm_portion'] = count / max_count
                items.append(item)

        items = [x for x in items if x['count'] > 0]
        items = sorted(items, key=lambda k: -k['count']) 
        longest_label = max([len(x['label']) for x in items])
        
        lines = []
        for x in items:
            line = self._prefix
            line += x['label'].ljust(longest_label) + "   " 
            line += render_percentage(x['portion']) + " "
            line += render_progress_bar(x['norm_portion'], char_full="*", char_empty=" ", prefix="", postfix="")
            line += " [%d]" % (x['count'])
            
            lines.append(line)
            
        lines.append(self._prefix + ("-" * 20))
        lines.append(self._prefix + ("TOTAL: %d" % self._total_count))
            
        return "\n".join(lines)