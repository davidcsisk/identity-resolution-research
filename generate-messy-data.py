import csv
import re
import random
from pathlib import Path

random.seed(42)

IN = Path('data-soft-join/sample-data-complete_100.csv')
OUT = Path('data-soft-join/sample-data-messy.csv')

def misspell_first(first):
    if len(first) > 2:
        i = 1
        return first[:i] + first[i+1] + first[i] + first[i+2:]
    return first + 'x'

def misspell_name(name):
    parts = name.split()
    parts[0] = misspell_first(parts[0])
    return ' '.join(parts)

def alt_email(email, idx, variant):
    local, domain = email.split('@')
    local_parts = local.split('.')
    first = local_parts[0]
    last = local_parts[1] if len(local_parts) > 1 else ''
    if variant == 0:
        return f"{first}.{last}{(idx%7)}@example.net"
    if variant == 1:
        return ''  # simulate missing email for variant 2
    return f"{first[0]}{last}@mail.example.org"


def alter_address(addr, idx, variant):
    m = re.match(r"(\d+)\s+(.*)", addr)
    if not m:
        return addr
    num = int(m.group(1))
    rest = m.group(2)
    # small deterministic change: +1 or -1
    delta = (idx % 2) * 2 - 1  # -1, +1 alternating
    if variant == 0:
        newnum = num + delta
        return f"{newnum} {rest}"
    if variant == 1:
        # abbrev street types
        return rest.replace('Street', 'St').replace('Rd', 'Rd.').replace('Ave', 'Ave.')
    return f"{num} {rest} Apt {(idx%20)+1}"


def alter_phone(phone, idx, variant):
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 10:
        return phone
    if variant == 0:
        # different separator
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    if variant == 1:
        # missing phone
        return ''
    return f"({digits[:3]}) {digits[3:6]}.{digits[6:]}"


rows = []
with IN.open(newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    for idx, r in enumerate(reader):
        for variant in range(3):
            nr = r.copy()
            # Always keep true_id
            nr['true_id'] = r['true_id']
            if variant == 0:
                # misspelled first name, altered email, slightly changed address
                nr['name'] = misspell_name(r['name'])
                nr['email'] = alt_email(r['email'], idx, 0)
                nr['address'] = alter_address(r['address'], idx, 0)
                nr['phone'] = alter_phone(r['phone'], idx, 0)
            elif variant == 1:
                # missing email, address abbreviation change, phone format same
                nr['name'] = r['name']
                nr['email'] = alt_email(r['email'], idx, 1)
                nr['address'] = alter_address(r['address'], idx, 1)
                nr['phone'] = r['phone']
            else:
                # name reversed, altered email, missing phone
                parts = r['name'].split()
                if len(parts) >= 2:
                    nr['name'] = f"{parts[-1]}, {' '.join(parts[:-1])}"
                else:
                    nr['name'] = r['name']
                nr['email'] = alt_email(r['email'], idx, 2)
                nr['address'] = alter_address(r['address'], idx, 2)
                nr['phone'] = alter_phone(r['phone'], idx, 2)

            # Introduce an extra deterministic missing/wrong field in ~40% of rows
            if (idx * 3 + variant) % 5 == 0:
                # blank either address or phone
                if ((idx + variant) % 2) == 0:
                    nr['address'] = ''
                else:
                    nr['phone'] = ''

            rows.append(nr)

# shuffle rows
random.shuffle(rows)

# write out
with OUT.open('w', newline='', encoding='utf-8') as fh:
    fieldnames = ['name','email','address','phone','true_id']
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Wrote {len(rows)} messy rows to {OUT}")
