"""Validate the onboarding artifact, independently of its content builder.

Uses only the standard library. It does not start services or project tests.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / 'StudyVault'
MANIFEST = json.loads((VAULT / '.tools/source-manifest.json').read_text(encoding='utf-8'))
FILES = sorted(VAULT.rglob('*.md'))
CONTENTS = {p: p.read_text(encoding='utf-8') for p in FILES}
BY_STEM = {}
for p in FILES:
    BY_STEM.setdefault(p.stem, []).append(p)
ERRORS = []
CHECKS = []
LINKS = {}

def require(condition, message):
    if not condition:
        ERRORS.append(message)

def root_file(path):
    candidate = (ROOT / path).resolve()
    require(candidate.is_relative_to(ROOT), '来源超出项目目录: ' + path)
    return candidate

def target_file(raw, current):
    target = raw.split('|', 1)[0].split('#', 1)[0].strip()
    if not target:
        return current
    candidate = VAULT / target
    if candidate.suffix != '.md':
        candidate = candidate.with_suffix('.md')
    if candidate in CONTENTS:
        return candidate
    candidates = BY_STEM.get(Path(target).stem, [])
    return candidates[0] if len(candidates) == 1 else None

for p, content in CONTENTS.items():
    rel = p.relative_to(VAULT).as_posix()
    front = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
    require(front is not None, rel + ': 缺少 YAML frontmatter')
    if front:
        for key in ('module', 'path', 'keywords'):
            require(re.search(r'^' + key + r':\s*\S', front[1], re.M), rel + ': 缺少 ' + key)
        keyword_line = re.search(r'^keywords:\s*(.*)', front[1], re.M)
        if keyword_line:
            require(not re.search(r'[\u4e00-\u9fff\uac00-\ud7af]', keyword_line[1]), rel + ': keywords 应为英文')
    require(not re.search(r'(?<![\w])[A-Za-z]:[\\/]|file://|/(?:Users|home|root|tmp)/', content), rel + ': 存在硬编码绝对文件路径')
    # Read actual standalone tag lines, excluding definitions and headings.
    actual_tags = []
    for line in content.splitlines():
        if re.fullmatch(r'#[a-z][a-z0-9-]*(?:\s+#[a-z][a-z0-9-]*)*', line):
            actual_tags.extend(x[1:] for x in line.split())
    require(bool(actual_tags), rel + ': 缺少内容标签')
    for tag in actual_tags:
        require(tag in MANIFEST['tags'], rel + ': 未注册标签 ' + tag)
    if any(t.startswith(('pattern-', 'api-')) for t in actual_tags):
        require(any(t.startswith('module-') for t in actual_tags), rel + ': 细节标签缺少 module 标签')
    require('## Related Notes' in content, rel + ': 缺少 Related Notes')
    resolved = []
    for match in re.finditer(r'\[\[([^\]\n]+)\]\]', content):
        target = target_file(match[1], p)
        require(target is not None, rel + ': 未解析 wiki-link [[' + match[1] + ']]')
        if target:
            resolved.append(target)
    LINKS[p] = set(resolved)
CHECKS.append(('笔记模板、相对路径与标签', len(FILES)))

question_total = 0
for module in MANIFEST['modules']:
    note = VAULT / module['folder'] / (module['title'] + '.md')
    practice = VAULT / '15-Exercises' / (module['title'] + '练习.md')
    require(note in CONTENTS, '缺少模块笔记: ' + module['title'])
    require(practice in CONTENTS, '缺少模块练习: ' + module['title'])
    if note not in CONTENTS or practice not in CONTENTS:
        continue
    content = CONTENTS[note]
    for section in ('Purpose', 'Key Files', 'Public Interface', 'Internal Flow', 'Dependencies', 'Configuration', 'Testing', 'Related Notes'):
        require('## ' + section in content, module['title'] + ': 缺少章节 ' + section)
    require('```text\n' in content, module['title'] + ': 缺少 ASCII 流程')
    require('```powershell\n' in content, module['title'] + ': 缺少测试命令')
    require(practice in LINKS[note] and note in LINKS[practice], module['title'] + ': 模块与练习未双向链接')
    require('module-' + module['id'] in content, module['title'] + ': 模块标签不匹配')
    for other_id in module['deps']:
        other = next(x for x in MANIFEST['modules'] if x['id'] == other_id)
        other_note = VAULT / other['folder'] / (other['title'] + '.md')
        require(other_note in LINKS[note] and note in LINKS[other_note], module['title'] + ': 依赖链接未双向 ' + other['title'])
    questions = re.findall(r'^## Exercise \d+ — .*?\[(\w+)\]\n(.*?)(?=^## Exercise|^> \[!summary\]|\Z)', CONTENTS[practice], re.M | re.S)
    require(len(questions) >= 5, module['title'] + ': 练习少于 5 题')
    question_total += len(questions)
    kinds = {kind for kind, _ in questions}
    require({'trace', 'config', 'debug', 'extend'}.issubset(kinds), module['title'] + ': 题型不足')
    for i, (_, body) in enumerate(questions, 1):
        require(body.count('> [!answer]- 查看答案') == 1, module['title'] + f': 第 {i} 题答案没有唯一折叠 callout')
        if '> [!answer]- 查看答案' in body:
            answer = body.split('> [!answer]- 查看答案', 1)[1].strip()
            require(bool(answer) and all(line.startswith('>') or not line.strip() for line in answer.splitlines()), module['title'] + f': 第 {i} 题答案泄露在 callout 外')
CHECKS.append(('主要领域与完整模块章节', len(MANIFEST['modules'])))
CHECKS.append(('练习及四类必要题型、中文折叠答案', question_total))

moc = VAULT / '00-Dashboard/AAAAGENT学习地图.md'
for p in FILES:
    if p != moc:
        require(p in LINKS[moc], 'MOC 未链接: ' + p.relative_to(VAULT).as_posix())
for section in ('Architecture Overview', 'Module Map', 'API Surface', 'Getting Started', 'Tag Index', 'Onboarding Path'):
    require('## ' + section in CONTENTS[moc], 'MOC 缺少 ' + section)
for tag in MANIFEST['tags']:
    require('`#' + tag + '`' in CONTENTS[moc], 'MOC 标签表缺少 ' + tag)
for name in ('系统架构', '请求流', '数据流与来源'):
    p = VAULT / '01-Architecture' / (name + '.md')
    require('```text\n' in CONTENTS[p], name + ': 缺少 ASCII 图')
CHECKS.append(('MOC 覆盖与 wiki-links', sum(len(v) for v in LINKS.values())))

for path, record in MANIFEST['sources'].items():
    source = root_file(path)
    require(source.is_file(), '来源不存在: ' + path)
    if not source.is_file():
        continue
    data = source.read_bytes()
    require(hashlib.sha256(data).hexdigest() == record['sha256'], '来源内容已变化，应复核笔记: ' + path)
    lines = data.decode('utf-8-sig').splitlines()
    require(len(lines) == record['lines'], '来源行数已变化: ' + path)
    for ref in record['references']:
        require(0 < ref['line'] <= len(lines), '定位行越界: ' + path)
        if ref['locator'] and 0 < ref['line'] <= len(lines):
            require(ref['locator'] in lines[ref['line'] - 1], '符号定位失效: ' + path)
CHECKS.append(('项目内来源文件、符号定位与 SHA256', len(MANIFEST['sources'])))

# Validate runnable examples against actual manifests, including selected tests.
module_scopes = {
    'code/desktop-pet': 'code/desktop-pet/package.json',
    'windows/code/desktop-pet': 'windows/code/desktop-pet/package.json',
    'windows/local-models': 'windows/local-models/package.json',
    't3-source': 't3-source/package.json',
}
script_count = 0
test_count = 0
for p, content in CONTENTS.items():
    for block in re.findall(r'```powershell\n(.*?)```', content, re.S):
        scope = None
        for line in block.splitlines():
            if line.startswith('Set-Location '):
                scope = line.split(' ', 1)[1].strip()
                require(scope in module_scopes, '命令工作目录未知: ' + scope)
            match = re.fullmatch(r'npm(?:\.cmd)? (?:run )?([\w:-]+)', line)
            if match and not match[1].startswith('--') and match[1] not in ('ci', 'install'):
                require(scope in module_scopes, p.name + ': npm 命令未指定子项目')
                if scope in module_scopes:
                    scripts = json.loads((ROOT / module_scopes[scope]).read_text(encoding='utf-8'))['scripts']
                    require(match[1] in scripts, p.name + ': 不存在 npm script ' + match[1])
                    script_count += 1
            if line.startswith('node --test ') and scope:
                for target in line.split()[2:]:
                    if target.startswith('dist/') and target.endswith('.js'):
                        source = target.removeprefix('dist/')[:-3] + '.ts'
                        require((ROOT / scope / source).is_file(), p.name + ': 定向测试来源不存在 ' + source)
                        test_count += 1
            vp = re.fullmatch(r'vp run (?:--filter (\S+) )?([\w:-]+)(?: .*)?', line)
            if vp:
                if vp[1]:
                    manifests = [ROOT / 't3-source/apps' / x / 'package.json' for x in ('server','web','desktop')]
                    manifests += [q for q in (ROOT/'t3-source/packages').glob('*/package.json')]
                    matches = [json.loads(q.read_text(encoding='utf-8')) for q in manifests if q.is_file()]
                    matches = [x for x in matches if x.get('name') == vp[1]]
                    require(len(matches) == 1 and vp[2] in matches[0].get('scripts', {}), p.name + ': vp filter/script 不存在 ' + line)
                else:
                    scripts = json.loads((ROOT/'t3-source/package.json').read_text(encoding='utf-8'))['scripts']
                    require(vp[2] in scripts, p.name + ': vp script 不存在 ' + vp[2])
                script_count += 1
CHECKS.append(('命令清单匹配与定向测试来源', f'{script_count} 条脚本 / {test_count} 个测试引用'))

report = {
    'date': MANIFEST['date'], 'baseline': MANIFEST['baseline'],
    'status': 'passed' if not ERRORS else 'failed',
    'notes': len(FILES), 'modules':len(MANIFEST['modules']), 'questions':question_total,
    'source_files':len(MANIFEST['sources']), 'checks':[{'name':name,'count':count} for name,count in CHECKS],
    'errors': ERRORS,
    'not_run':['project-builds-and-tests','live-models','native-apps-and-devices','obsidian-rendering'],
}
(VAULT/'.tools/validation-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
status = '通过' if not ERRORS else '未通过'
table = f'状态：**{status}**。源码基线：`{MANIFEST["baseline"][:7]}`。\n\n| 自动检查 | 数量 |\n| --- | --- |\n'
table += '\n'.join(f'| {name} | {count} |' for name,count in CHECKS)
if ERRORS:
    table += '\n\n' + '\n'.join('- '+e for e in ERRORS)
table += '\n\n机器可读报告：`StudyVault/.tools/validation-report.json`。此结果只覆盖学习库本身。'
quality = VAULT/'00-Dashboard/建库自检.md'
quality_text = quality.read_text(encoding='utf-8')
quality.write_text(re.sub(r'<!-- validation-results:start -->.*?<!-- validation-results:end -->',
                         '<!-- validation-results:start -->\n'+table+'\n<!-- validation-results:end -->',
                         quality_text, flags=re.S), encoding='utf-8', newline='\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(1 if ERRORS else 0)
