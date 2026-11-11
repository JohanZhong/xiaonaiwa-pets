# Installation / 安装与排错

## Codex desktop

The folder format follows the working example in [timerring/codex-pet-naiwa](https://github.com/timerring/codex-pet-naiwa). It is not an official OpenAI compatibility guarantee.

每个宠物目录必须同时包含 `pet.json` 和 `spritesheet.webp`，不能只复制图片或把整个仓库当作宠物目录。

默认目录为 `$CODEX_HOME/pets`；未设置时使用用户主目录下的 `.codex/pets`。应用提供 **Open folder** 时，以它打开的实际目录为准。

```text
pets/
├── xiaonaiwa-2d/
│   ├── pet.json
│   └── spritesheet.webp
└── xiaonaiwa-3d/
    ├── pet.json
    └── spritesheet.webp
```

Windows:

```powershell
py -3 scripts/install.py --variant all
```

macOS / Linux:

```bash
python3 scripts/install.py --variant all
```

自定义目录 / Custom directory:

```bash
python scripts/install.py --variant 2d --dest /path/to/pets
```

安装器兼容 Python 3.9+，不需要 Pillow。只有素材校验和开发工具需要 `requirements-dev.txt`。

## Existing versions / 已有版本

同名文件夹默认不会覆盖。确认要升级时执行 `--force`：原目录会先保留为 `xiaonaiwa-2d.backup-时间戳`。安装失败时脚本尝试恢复原目录，不删除其他宠物。

要回滚：关闭使用该宠物的应用，将新版目录移到别处，再把备份恢复为原目录名。要卸载：通过文件管理器移走对应宠物目录，并在应用中刷新。

## Troubleshooting / 常见问题

| 现象 | 检查方式 |
| --- | --- |
| 没有 Pets / Custom pets 入口 | 确认客户端提供自定义宠物支持；本仓库不修改或解锁客户端功能 |
| 列表没有小奶蛙 | 检查目录是否多嵌套一层、两个必需文件是否齐全，刷新或重启客户端 |
| 校验失败 | 重新下载官方 Release；不要跳过校验继续安装 |
| 安装路径不对 | 使用应用 Open folder 返回的目录，传给 `--dest` |
| Linux 没有对应桌面客户端 | 安装器测试仅表示文件操作兼容，不代表桌面应用在该平台可用 |
| GIF 看起来颜色有层次断带 | 使用全彩 WebP 或 MP4 预览，实际素材采用无损导出 |
| 动画仍有逐帧感 | 客户端固定状态帧数与时长；本项目未修改客户端播放器 |
| Work Pets 中没出现 | 本地复制不会同步；通过 Pets 插件另行创建 |

## ChatGPT Work and legacy import

Use `work-spritesheet.png` for the supported v2 Pets workflow. Its 11 rows include pointer-facing poses. Use `legacy-v1.png` only if your importer explicitly requires 1536 × 1872. Both are PNGs with transparency; do not upload a README preview as a sprite sheet.

The repository contains no user account IDs, upload sessions or private service URLs. Your own installation creates your own pet entry.
