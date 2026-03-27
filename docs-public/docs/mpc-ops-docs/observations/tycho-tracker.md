# How to Submit Astrometry Using Tycho Tracker

Tycho Tracker is software developed by Daniel Parrott that helps astronomers detect and measure moving celestial objects like asteroids and comets. The tool employs synthetic tracking, enabling detection of faint objects through stacking multiple exposures (minimum 11) to enhance signal-to-noise ratios. Synthetic tracking allows detection of objects even when the motion is unknown by combining thousands of potential stacking combinations.


## Current Usage and Concerns

Both amateur and professional astronomers use Tycho Tracker extensively. 
The Catalina Sky Survey team integrated it into their operations, finding it valuable for extracting asteroids from crowded fields. 
However, the MPC is now receiving an increasing volume of observations, and a significant minority of these unfortunately 
contain false detections.

!!! warning
    Submitting false tracklets for NEOCP objects or short-arc designated objects 
    can distort orbital calculations and cause objects to be lost entirely.


## Before Submitting

- Read the [Tycho Tracker documentation](https://www.tycho-tracker.com/links) thoroughly
- Complete available [Tycho Tracker tutorials](https://www.tycho-tracker.com/links)


## Signal-to-Noise Standards

The most significant issue involves inappropriate use of Tycho Tracker to pull out phantom detections from random noise. Best practices include:

- Acquire sufficient images (typically 20+) for strong SNR
- Implement dithering — described as "absolutely essential" by the CSS Team
- Apply high confidence thresholds before detection classification


## Common Misconceptions

Users should understand that completely erroneous observations can easily fit to a short discovery arc. Crucially, the fact that observations fit in FindOrb or a similar orbit determination tool does **not** mean the detection is positive.

**Do not submit marginal or noisy detections.** High SNR with clear visibility is required for submission.


## SNR Guidance

| SNR Level | Action |
|-----------|--------|
| **Good SNR** — objects clearly visible | Submit confidently |
| **Marginal** — objects lack clear visibility | Request peer or MPC review before submitting |
| **Noisy** — objects barely visible, very low SNR | Do not submit |


## Acknowledgments

Documentation was developed with support from the CSS Team (David Rankin and Carson Fuls) and Daniel Parrott.
