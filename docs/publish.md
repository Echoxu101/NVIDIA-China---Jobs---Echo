# 发布到 GitHub

当前仓库：[NVIDIA-China---Jobs---Echo](https://github.com/Echoxu101/NVIDIA-China---Jobs---Echo)

下面的网页步骤适用于将这套文件发布到其他新仓库。

建议描述：`按 skillset 导航的 NVIDIA 技术岗位合集｜GPU / AI Performance / LLVM / Infrastructure / System Software / Autonomous Vehicles`

## 通过网页上传

1. 登录 GitHub，点击右上角 **+ → New repository**。
2. 输入仓库名与描述；若希望候选人直接浏览，选择 **Public**。也可先选择 **Private** 预览。
3. 创建空仓库，不勾选自动创建 README、.gitignore 或 License。
4. 选择 **uploading an existing file**，解压下载的 ZIP，将 `nvidia-tech-careers` 文件夹内的文件和子目录拖入上传区。README 应位于仓库根目录。
5. 检查目录层级并提交。提交信息可填 `Add skill-based technical careers guide`。

隐藏目录 `.github` 包含可选的信息更正模板。若网页文件选择器不显示隐藏目录，可使用下面的 Git 命令上传全部内容。

## 通过 Git 上传

在解压后的 `nvidia-tech-careers` 目录打开终端，执行：

```bash
git init -b main
git add .
git commit -m "Add skill-based technical careers guide"
```

在 GitHub 创建空仓库后，复制其 HTTPS 地址，将下面的占位地址替换为真实地址：

```bash
git remote add origin https://github.com/Echoxu101/NVIDIA-China---Jobs---Echo.git
git push -u origin main
```

GitHub 如提示认证，请按本机 Git / GitHub 的认证流程完成登录。

## 发布后

- 查看 README 中的岗位链接及联系邮箱。
- 可在仓库 About 添加 `nvidia`、`careers`、`gpu`、`llvm`、`system-software` 等 topics。
- 分享仓库主页即可；README 就是候选人的入口。
