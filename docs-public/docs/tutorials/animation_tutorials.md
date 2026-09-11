# Orbit Animations

Tutorials on turning MPC orbit data into animations — how to simulate the motion, how to choose a frame of reference that makes the physics visible, and how to render the result as video for the web. Each tutorial notebook produces the stand-alone animations shown below it.

These build on the simpler, static tutorials in [Working with Orbits](orbit_tutorials.md) — fetching an orbit from the MPC, integrating it with REBOUND and ASSIST, and plotting it — so start there if those steps are new to you.

<div id="contents-grid"></div>

 - [Animating Minimoons: Earth's Temporarily Captured Asteroids](notebooks/mpc_tutorial_orbit_animation_minimoons.ipynb)
 - [Watching the Kirkwood Gaps Form](notebooks/mpc_tutorial_orbit_animation_kirkwood.ipynb)

---

## Minimoons: Earth's temporarily captured asteroids

Three real minimoons, simulated with [ASSIST](https://assist.readthedocs.io/) from their MPC orbits and drawn in the frame co-rotating with the Sun–Earth line: Earth at the centre, the Moon and its orbit, Earth's Hill sphere with the L1 and L2 gateways, and the object's path growing with time; beside it, the object's distance from Earth against date, with the gravitationally bound interval shaded. Produced by the [minimoon animation tutorial](notebooks/mpc_tutorial_orbit_animation_minimoons.ipynb).

### 2006 RH120 — a temporarily captured orbiter (2006–2007)

<video controls loop muted playsinline width="100%" poster="../animations/minimoon_2006_RH120_rotating.png">
  <source src="../animations/minimoon_2006_RH120_rotating.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 2020 CD3 — captured unseen in 2017, discovered in 2020

<video controls loop muted playsinline width="100%" poster="../animations/minimoon_2020_CD3_rotating.png">
  <source src="../animations/minimoon_2020_CD3_rotating.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 2024 PT5 — a two-month fly-through (2024)

<video controls loop muted playsinline width="100%" poster="../animations/minimoon_2024_PT5_rotating.png">
  <source src="../animations/minimoon_2024_PT5_rotating.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 2006 RH120 seen from the Sun

The same capture in heliocentric coordinates with the axes fixed in space. 
The camera starts on the whole orbit, glides in to follow Earth as the asteroid catches up, holds through the bound phase — where the loops trace a slowly turning rosette — and pulls back out after the release.

<video controls loop muted playsinline width="100%" poster="../animations/minimoon_2006_RH120_heliocentric.png">
  <source src="../animations/minimoon_2006_RH120_heliocentric.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


## The Kirkwood gaps forming

A gap-free synthetic asteroid belt of 4,000 test particles under the Sun, Jupiter and Saturn, integrated for ten million years with REBOUND. Left: the (semi-major axis, eccentricity) plane, where the mean-motion resonances pump eccentricities until orbits cross Mars's and the particles are removed; right: the histogram of survivors with the real belt from MPCORB underneath. The 3:1 and 5:2 gaps and the ν₆ inner edge open within the first million years, the 7:3 follows slowly, and the 2:1 gap only begins to empty after three million years. Produced by the [Kirkwood gaps animation tutorial](notebooks/mpc_tutorial_orbit_animation_kirkwood.ipynb).

<video controls loop muted playsinline width="100%" poster="../animations/kirkwood_gaps_forming.png">
  <source src="../animations/kirkwood_gaps_forming.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

Related static tutorials in [Working with Orbits](orbit_tutorials.md): 

 - [From MPC Orbit to Ephemeris-Quality Integration with ASSIST](notebooks/mpc_tutorial_orbit_to_assist.ipynb) (the integration set-up used here)
 - [From MPC Orbit to N-Body Simulation](notebooks/mpc_tutorial_orbit_to_rebound.ipynb), 
 - [Earth's Co-orbital Companions](notebooks/mpc_tutorial_orbit_earth_coorbitals.ipynb) (the same rotating frame, for horseshoe and quasi-satellite orbits), and 
 - [Reference Frames for Solar System Dynamics](notebooks/mpc_tutorial_orbit_frames.ipynb).
 - [The Kirkwood Gaps](notebooks/mpc_tutorial_orbit_kirkwood.ipynb) (the static view of the gaps the second animation reproduces)

[//]: # (The MP4 files above, and GIF versions of each animation, are written by the notebook into )

[//]: # (the `animations/` folder next to it, so re-running the notebook for a new object produces a drop-in addition to this page.&#41;)
