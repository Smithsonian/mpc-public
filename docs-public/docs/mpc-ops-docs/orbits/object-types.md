# Object Type Definition

The Minor Planet Center defines some broad classes of objects. 
These classes are encoded in the `object_type` field of the MPCORB format and the `object_type` property of the MPC_ORB JSON format. 
The following table lists the object types and their assigned numbers.

---

## Object Type Classification

| Object Type | Assigned Number | Definition |
|-------------|-----------------|------------|
| Minor Planet | 0 | Object in orbit around the Sun that is exclusively classified as neither a planet nor a comet. Includes asteroids, Mars-crossers, main-belt asteroids, Jupiter trojans, centaurs, and trans-Neptunian objects. |
| Minor Planet (Binary) | 1 | System of two asteroids orbiting their common barycenter. |
| [Past Impactor](https://data.minorplanetcenter.net/explorer/?tab=Lists&list=Past+Impactors) | 6 | Object that has impacted with the Earth and that has been identified before the impact, e.g. 2014 AA. |
| Comet | 10 | Body made of rock and ice, typically a few kilometres in diameter, which orbits the Sun. |
| Comet (Fragment) | 11 | Piece of comet that has broken off from the main body. |
| [Dual Status (Minor Planet and Comet)](https://data.minorplanetcenter.net/explorer/?tab=Lists&list=Dual-Status+Objects) | 20 | Object with both minor planet and cometary designation; initially classified as a minor planet but showing cometary activity. |
| Natural Satellite (of planet) | 30 | Object well within the Hill sphere of a planet and appears gravitationally bound. |
| Natural Satellite (of minor planet) | 40 | Object that has been measured to orbit around another minor planet or the center of mass of a minor planet system. |
| Interstellar Object | 50 | Object that originates from outside the solar system and is not gravitationally bound to the Sun. |
