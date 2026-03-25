# Export Format for Natural Satellite Orbits

This page describes the format used for natural satellite orbital elements, as used on
the Minor Planet Center's Natural Satellites Observers Page. Orbital elements for natural
satellites are planet-barycentric.

---

## Column Specifications

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>1&ndash;12</td><td>a12</td><td>Number or provisional designation (<a href="../designations/packed-designations.md">packed form</a>)</td></tr>
<tr><td>14&ndash;18</td><td>a5</td><td>Epoch (<a href="../designations/packed-dates.md">packed form</a>, .0 TT)</td></tr>
<tr><td>20&ndash;32</td><td>f13.5</td><td>Time of perihelion (JDT)</td></tr>
<tr><td>34&ndash;42</td><td>f9.5</td><td>Argument of perihelion, J2000.0 (degrees)</td></tr>
<tr><td>44&ndash;52</td><td>f9.5</td><td>Longitude of ascending node, J2000.0 (degrees)</td></tr>
<tr><td>54&ndash;62</td><td>f9.5</td><td>Inclination to ecliptic, J2000.0 (degrees)</td></tr>
<tr><td>64&ndash;72</td><td>f9.7</td><td>Orbital eccentricity</td></tr>
<tr><td>74&ndash;82</td><td>f9.7</td><td>Periapsis distance (AU)</td></tr>
<tr><td>84&ndash;85</td><td>i2</td><td>Central body (05=Jupiter, 06=Saturn, 07=Uranus, 08=Neptune)</td></tr>
<tr><td>87&ndash;91</td><td>f5.2</td><td>Absolute magnitude, <em>H</em></td></tr>
<tr><td>93&ndash;98</td><td>i6</td><td>Observed arc (days)</td></tr>
<tr><td>100&ndash;104</td><td>i5</td><td>Number of observations</td></tr>
<tr><td>106&ndash;108</td><td>a3</td><td>Orbit computer</td></tr>
<tr><td>110&ndash;118</td><td>a9</td><td>Publication reference</td></tr>
<tr><td>120&ndash;124</td><td>a5</td><td>Date (UT) of first observation (<a href="../designations/packed-dates.md">packed form</a>)</td></tr>
<tr><td>126&ndash;130</td><td>a5</td><td>Date (UT) of last observation (<a href="../designations/packed-dates.md">packed form</a>)</td></tr>
<tr><td>132&ndash;136</td><td>f5.2</td><td>RMS residual (&Prime;)</td></tr>
<tr><td>138&ndash;140</td><td>a3</td><td>Coarse indicator of perturbers</td></tr>
<tr><td>142&ndash;144</td><td>a3</td><td>Precise indicator of perturbers</td></tr>
<tr><td>146+</td><td>a</td><td>Satellite name</td></tr>
</tbody>
</table>
