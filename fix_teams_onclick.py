import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Fix 1: remove safeId line and replace JSON.stringify onclick with numeric idx
old = "const safeId=f.id.replace(/'/g,\"\\\\'\");\n      html+=`<div onclick=\"state.teamsFranchise=${JSON.stringify(f.id)};render()\""
new = "html+=`<div onclick=\"state.teamsFranchise=${f.idx};render()\""

if old in html:
    html = html.replace(old, new)
    print("Fixed onclick to use numeric index")
else:
    # Try without safeId line (may already be removed)
    old2 = '`<div onclick="state.teamsFranchise=${JSON.stringify(f.id)};render()"'
    new2 = '`<div onclick="state.teamsFranchise=${f.idx};render()"'
    if old2 in html:
        html = html.replace(old2, new2)
        print("Fixed JSON.stringify onclick")
    else:
        print("Pattern not found - checking current state:")
        idx = html.find('teamsFranchise=')
        while idx != -1:
            print(f"  pos {idx}:", repr(html[idx:idx+60]))
            idx = html.find('teamsFranchise=', idx+1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done")
