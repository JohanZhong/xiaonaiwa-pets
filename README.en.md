# Xiaonaiwa Pets

**A little buttery-yellow companion, in two styles.**

[简体中文](README.md) · [Download](https://github.com/JohanZhong/xiaonaiwa-pets/releases/latest) · [Install](docs/INSTALL.md) · [Report an issue](https://github.com/JohanZhong/xiaonaiwa-pets/issues/new/choose)

| Classic 2D | Refined 3D |
| :---: | :---: |
| ![Classic blink](docs/previews/2d/idle.gif) | ![3D idle](docs/previews/3d/idle.gif) |

Two independently installable companions, nine animation states and sixteen look directions each. The classic edition preserves the original poses and refines the eyelid transitions. The 3D edition has soft toy materials, rounded volume and glossy eyes. “2D” names the classic edition; its artwork still has gentle shading.

## Install

Download the ZIP from [Releases](https://github.com/JohanZhong/xiaonaiwa-pets/releases/latest). In a Codex desktop build with custom-pet support, open **Settings → Pets → Custom pets → Open folder**. Copy `pets/xiaonaiwa-2d` and `pets/xiaonaiwa-3d` into that folder, refresh, and select a pet.

Alternatively, with Python 3.9+:

```bash
python scripts/install.py --variant all
```

Use `--variant 2d` or `--variant 3d` for one edition. The installer verifies SHA-256 hashes before copying, refuses existing folders by default and backs them up when `--force` is requested. It does not access the network or modify application settings. Use `--dest` for a custom pet directory. See [installation and troubleshooting](docs/INSTALL.md).

## ChatGPT Work Pets

Desktop and Work Pets are managed separately. Use each edition’s `work-spritesheet.png` with a Pets-enabled assistant, asking it to validate and create a new pet while preserving existing pets. Both v2 PNGs passed the Pets service preflight during production. `legacy-v1.png` is a nine-row fallback for older importers; it omits directional gaze. Availability and UI entry points depend on the client.

## Preview and format

[Classic full-color animation](docs/previews/2d/all-states.webp) · [3D full-color animation](docs/previews/3d/all-states.webp) · [Animation contract](docs/ANIMATION.md)

Previews use the platform’s fixed frame timings, with no interpolated frames. V2 is 1536 × 2288 pixels, arranged in 192 × 208 cells. Each edition has 57 action frames and 16 look poses. GIF previews have palette limitations; WebP and MP4 previews preserve richer color.

## Verification

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_release.py
```

CI checks file hashes, metadata, transparent cells, required frame occupancy and lossless export equivalence on Windows, macOS and Linux. Installer tests cover both editions, overwrite protection, backups and rejection of corrupted files. Frame-level review is complete; this is not a claim of UI testing in every Codex release.

## Fan work and credits

This is an unofficial fan project, unaffiliated with OpenAI or the character’s rights holders. Code is MIT-licensed; character art and third-party rights are **not** included in that license. See [ASSET_NOTICE](ASSET_NOTICE.md). Public availability does not establish permission for commercial reuse.

Repository organization and installation UX were inspired by [timerring/codex-pet-naiwa](https://github.com/timerring/codex-pet-naiwa). No sprite artwork from that repository was copied. These assets were produced from user-supplied character references and built-in image generation, followed by selection and validation.

Contributions and reproducible reports are welcome: [CONTRIBUTING](CONTRIBUTING.md). If this little companion improves your workday, a Star helps others find it.
