# news-image-20261124-001

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Fajargh/news-image-20261124-001/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Fajargh/news-image-20261124-001/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Sum up 24 November's world news in one image: a one-page newspaper front page — "THE WORLD TODAY — Tuesday, 24 November 2026" — drawn procedurally with Pillow. Six real stories reported on 24 November 2026: Nvidia reinstates Jensen Huang as CEO as shares surge 31%; the COP31 climate talks collapse with no deal; Ukraine says it sank a Russian warship off Libya; NATO sends early-warning jets to Poland; a factory fire in Indonesia kills at least 24; and the World Chess Championship opens in Geneva with Gukesh defending his title. An IN BRIEF strip covers Gaza, US sanctions on Iran's shadow banking, the Iowa explosives pause, the India–New Zealand Test draw, and CrowdStrike's deal to buy Zscaler.

## Run it

```sh
python3 main.py
```

The program draws the front page and writes it to `/output/entry.png` (1024×1024 PNG, under 1 MiB), then validates the file — PNG signature, dimensions, size — and checks that a fresh render is byte-identical. Set `MAKEFUN_OUTPUT_DIR` to choose another output directory.

---

<sub>Entered on [make.fun](https://make.fun/?ref=8cvj6bwy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
