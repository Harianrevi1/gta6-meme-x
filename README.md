# 13 Years Waiting For This Bar To Move

[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Harianrevi1/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Harianrevi1/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

An entry for the [make.fun bounty "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01) — a GTA 6 meme about the thirteen-year wait since GTA V, drawn as a loading bar on a Leonida beach at sunset.

## The meme

GTA VI finally hits 100% on its download bar after 13 years of waiting — and while the player is busy in Leonida, their AI agent is out earning real money in bounties on make.fun. The make.fun ghost watches from the sand, holding its magenta star coin.

`meme.png` (1024×1024, drawn with Pillow by `make_meme.py`) shows:

- the headline "13 YEARS WAITING FOR THIS BAR TO MOVE" over a Vice City sunset,
- a "GTA VI — LEONIDA" panel with the green bar reading "100% — FINALLY OUT",
- the make.fun ghost mascot with its sparkle eyes and star coin,
- the line "make.fun • MY AGENT EARNS WHILE I PLAY" along the bottom.

Every caption stays readable when the picture is shrunk to 480×480, the size the judge reads it at.

## The post

The meme is posted on X from the public account @bussinessclas16, with the picture attached first. The post text (see `POST.json` for the post's address) carries a link to make.fun, a tag of @makefunai, the entry's play code, and the pitch that agents earn real money in bounties on make.fun. The post stays up and the account stays public until the results are out.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` from the repository root to `$MAKEFUN_OUTPUT_DIR` (default `/output`). That is all it does — the house reads the post itself from X.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

It prints nothing on success.
