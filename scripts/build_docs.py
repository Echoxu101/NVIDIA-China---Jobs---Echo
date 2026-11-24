"""Render candidate-facing Markdown from data/roles.json (Python 3, no dependencies)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    data = json.loads((ROOT / 'data/roles.json').read_text(encoding='utf-8'))
    roles = data['roles']
    by_id = {r['id']: r for r in roles}
    assert len(roles) == len(by_id), 'Duplicate job IDs'
    categories = {c['id']: c for c in data['categories']}
    for role in roles:
        assert role['category'] in categories, role['id']
        assert role['locations'], role['id']
    def link(r):
        return f"[{r['id']}｜{r['title']}](roles/{r['id']}.md)"
    def table(items):
        lines = ['| 职位 ID | 岗位 | 地点 |', '| --- | --- | --- |']
        lines += [f"| [{r['id']}](roles/{r['id']}.md) | {r['title']} | {' / '.join(r['locations'])} |" for r in items]
        return '\n'.join(lines)
    text = f'''# NVIDIA 技术岗位导航

**从你的 skillset 出发，找到更适合的技术机会。**

GPU · AI Performance · Profiling · Compiler · LLVM · Infrastructure · System Software · Autonomous Vehicles · Solutions Architecture

本仓库按技术方向整理 **{len(roles)} 个岗位、{len(categories)} 类机会**，覆盖上海、深圳和北京。你可以先按技能定位方向，再进入岗位详情了解工作内容和适合背景。

这些机会涉及硬件、系统软件、AI workload、编译器、自动驾驶平台和真实业务场景的交叉地带，适合希望深入技术、参与平台和系统建设的同学。

> 整理日期：{data['updated_at']}。内容来自 Echo Xu 提供的[招聘帖子]({data['source_url']})，属于岗位导读；岗位是否开放、完整要求与地点以 [NVIDIA Careers]({data['careers_url']}) 当前信息为准。本仓库不是 NVIDIA 官方招聘网站。

## 快速入口

- [按技能找岗位](#按技能找岗位)
- [按技术方向浏览](#按技术方向浏览)
- [按城市浏览](docs/locations.md)
- [投递与联系](#投递与联系)

## 按技能找岗位

下表为原帖中的方向建议，帮助初步定位，不代表每个岗位都要求具备整组技能。具体背景与加分项请查看岗位详情。

| 你的技能 / 技术方向 | 可以重点看的岗位 |
| --- | --- |
'''
    for match in data['skill_matching']:
        text += f"| {match['skillset']} | " + '<br>'.join(link(by_id[j]) for j in match['role_ids']) + ' |\n'
    text += '\n## 按技术方向浏览\n'
    for cat in data['categories']:
        text += f"\n### {cat['name']}\n\n{cat['audience']}\n\n"
        text += table([r for r in roles if r['category'] == cat['id']]) + '\n'
    text += f'''
## 投递与联系

1. 打开 [NVIDIA Careers]({data['careers_url']})，搜索职位 ID（例如 `JR2016747`），查看完整 JD 并完成投递。
2. 如希望进一步了解岗位，可邮件联系 [Echo Xu](mailto:{data['contact']['email']})：**{data['contact']['email']}**。
3. 邮件中可以注明感兴趣的职位 ID、目前所在地及主要技术方向，便于沟通。

建议邮件主题：`职位咨询｜JR2016747｜姓名｜GPU Profiling / CUDA`

也欢迎把仓库分享给从事大模型训练、分布式系统、性能优化、数据平台、系统软件、GPU Profiling、HPC 或 AI Infra 的朋友。

## 仓库内容与维护

| 路径 | 内容 |
| --- | --- |
| `roles/` | 每个岗位的工作内容、背景与适合人群 |
| [docs/locations.md](docs/locations.md) | 上海 / 深圳 / 北京岗位索引 |
| [data/roles.json](data/roles.json) | 结构化岗位数据与技能映射 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 如何更新岗位与提交信息更正 |
| [docs/publish.md](docs/publish.md) | 将这套文件发布到 GitHub 的步骤 |

维护时修改 `data/roles.json`，再运行 `python3 scripts/build_docs.py`，即可同步更新 README、城市索引和岗位详情。
'''
    outputs = {ROOT / 'README.md': text}
    for r in roles:
        outputs[ROOT / 'roles' / f"{r['id']}.md"] = f'''# {r['title']}

[返回岗位导航](../README.md) · [按城市浏览](../docs/locations.md)

| 项目 | 信息 |
| --- | --- |
| 职位 ID | `{r['id']}` |
| 工作地点 | {' / '.join(r['locations'])} |
| 技术方向 | {categories[r['category']]['name']} |
| 检索关键词 | {' · '.join(r['keywords'])} |
| 整理日期 | {data['updated_at']} |

## 你会做什么

{r['work']}

## 我们希望看到的背景

{r['background']}

## 适合什么样的同学

{r['fit']}

## 投递与咨询

前往 [NVIDIA Careers]({data['careers_url']})，搜索 **{r['id']}**，查看完整 JD 并投递。

也可联系 [Echo Xu](mailto:{data['contact']['email']})（{data['contact']['email']}），邮件中注明职位 ID、所在地和技术方向。

---

内容依据 [Echo Xu 的招聘帖子]({data['source_url']})及其提供的正文整理。关键词用于帮助浏览，不等于完整任职要求；岗位状态、完整要求与地点请以官网当前信息为准。
'''
    locations = '# 按城市找岗位\n\n[返回岗位导航](../README.md)\n\n多地点岗位会同时出现在对应城市下。\n'
    for city in ['上海', '深圳', '北京']:
        subset = [r for r in roles if city in r['locations']]
        locations += f'\n## {city}（{len(subset)} 个）\n\n'
        locations += table(subset).replace('(roles/', '(../roles/') + '\n'
    locations += '\n地点依据原帖整理，以 NVIDIA Careers 当前信息为准。\n'
    outputs[ROOT / 'docs/locations.md'] = locations
    return outputs

if __name__ == '__main__':
    for path, content in render().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    print('Generated README, role pages and city index.')
