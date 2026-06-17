CUSTOM ASSETS — Pokémon: The Three Stolen Lights
=================================================

This game runs fully with its built-in original music and art.
If you want to use your OWN files (for your private/internal build),
drop them in this "assets" folder and point the game at them.

HOW TO ENABLE A FILE
--------------------
1. Put your file in this folder, e.g.  assets/sylveon.png
2. Open ../index.html and find the "CUSTOM ASSETS" block near the top.
3. Set the matching path. Examples:

      mon.sylveon  = 'assets/sylveon.png'
      mon.eevee    = 'assets/eevee.png'
      char.oen     = 'assets/oen.png'
      music.battle = 'assets/battle.mp3'
      music.route  = 'assets/route.ogg'
      sfx.hit      = 'assets/hit.wav'
      sfx.mBite    = 'assets/bite.wav'

Anything left as ''  keeps the built-in original — so you can mix and
match (e.g. custom Pokémon images but keep the original music).

WHAT YOU CAN REPLACE
--------------------
mon.*    Pokémon images (PNG with transparency works best).
         Keys: eevee, jolteon, flareon, sylveon, rattata, zubat,
         magnemite, voltorb, koffing, houndour, ekans, murkrow, persian.
         Drawn centred on a square; feet sit near the bottom.

char.*   Overworld people (small ~16x18 sprites, static/front-facing).
         Keys: oen, oak, asst, kid, grunt, rook.

music.*  Looping background tracks (.mp3 / .ogg / .wav).
         Keys: lab, route, tense, battle, warm, emotion.

sfx.*    One-shot sound effects (.wav / .mp3 / .ogg).
         Keys: hit, hitSuper, hitWeak, faint, heal, win, confirm,
         cursor, ballopen, throw, battlestart, lowhp, door, spark,
         mTackle, mQuick, mBite, mSwift, mFire, mZap.
         (mXxx = the sound for that specific move animation.)

NOTES
-----
- Sound only starts after your first key press (browser autoplay rule).
- Press M in-game to mute. Esc opens the pause menu (Save / Mute / Title).
- Missing files are ignored gracefully; the game never breaks.
- IMPORTANT: only add files you have the right to use. Copyrighted game
  rips were not included for that reason — sourcing files is up to you.
