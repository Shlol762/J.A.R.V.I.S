import json
import re
import demoji


def progress_bar(progress, total, replaced, bar_len=50, title='Please wait'):
    percent = 100 * (progress/float(total))
    bounds_colour = "33;2m" if progress != total else "32;1m"
    done = round(percent*bar_len/100)
    if progress == total:
        _percent = 100 * (replaced/float(total))
        if _percent <= 33:
            bounds_colour = "31;1m"
        elif 34 < _percent <= 66:
            bounds_colour = "33;1m"
        done = round(_percent*bar_len/100)
    togo = bar_len-done
    bar = '\x1b[0;92;1m' + ('█' * int(done)) + f'\x1b[0;{"31;2m" if progress == total else "33;2m"}' + ('█' if progress == total else '-') * int(togo)
    print('\n' if progress ==0 else '\r'+f'\t{title}: \x1b[{bounds_colour}|{bar}\x1b[0;{bounds_colour}| \x1b[0;35m{round(percent,1):.2f}\x1b[0m% '
          f'\x1b[32;1m{progress: >5}\x1b[0m/\x1b[{bounds_colour}{total: <5}\x1b[0m | Replaced \x1b[92;1m{replaced: >4}\x1b[0m | '
          f'Not found \x1b[31m{progress-replaced:>4}\x1b[0m', end='\r' if progress != total else '\n')

if __name__ == '__main__':

    path = "C:/Users/Shlok/Downloads/messages.json"

    with open(path, 'r') as f:
        messages = json.load(f)

    with open("C:/Users/Shlok/Downloads/dump - Copy.txt", encoding='utf8') as f:
        dump = f.read()


    not_found = ''

    total_replaced = 0
    for channel, msgs in messages.items():
        print(channel + ':', end='')
        total_ = len(msgs)
        i = 0
        ir = 0
        progress_bar(i, total_, ir)
        for msg in msgs:
            # if len(msgs) > 100: break
            if match := re.search(rf'([0-9]\) {msg.lower()}\n)', dump):
                dump = dump.replace(match.group(), '', 1)
                ir += 1
            else: not_found += f'0) {msg.lower()}\n'
            i += 1
            total_replaced += 1
            progress_bar(i, total_, ir)

        print(total_replaced)


    with open("C:/Users/Shlok/Downloads/new_dump.txt", 'w', encoding='utf8') as f:
        f.write(dump)

    with open("C:/Users/Shlok/Downloads/not_found.txt", 'w', encoding='utf8') as f:
        f.write(not_found)
