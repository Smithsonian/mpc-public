# Export Format for Minor-Planet Orbits

This page describes the format used for both unperturbed and perturbed orbits of minor
planets. These are the formats used in the Extended Computer Service and in the Minor
Planet Ephemeris Service. Orbital elements for minor planets are heliocentric.

---

## Column Specifications

The column headed `F77` indicates the Fortran 77/90/95/2003/2008 format specifier for
reading the specified values.

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>1&ndash;7</td><td>a7</td><td>Number or provisional designation (in <a href="../designations/packed-designations.md">packed form</a>)</td></tr>
<tr><td>9&ndash;13</td><td>f5.2</td><td>Absolute magnitude, <em>H</em></td></tr>
<tr><td>15&ndash;19</td><td>f5.2</td><td>Slope parameter, <em>G</em></td></tr>
<tr><td>21&ndash;25</td><td>a5</td><td>Epoch (in <a href="../designations/packed-dates.md">packed form</a>, .0 TT)</td></tr>
<tr><td>27&ndash;35</td><td>f9.5</td><td>Mean anomaly at the epoch, in degrees</td></tr>
<tr><td>38&ndash;46</td><td>f9.5</td><td>Argument of perihelion, J2000.0 (degrees)</td></tr>
<tr><td>49&ndash;57</td><td>f9.5</td><td>Longitude of the ascending node, J2000.0 (degrees)</td></tr>
<tr><td>60&ndash;68</td><td>f9.5</td><td>Inclination to the ecliptic, J2000.0 (degrees)</td></tr>
<tr><td>71&ndash;79</td><td>f9.7</td><td>Orbital eccentricity</td></tr>
<tr><td>81&ndash;91</td><td>f11.8</td><td>Mean daily motion (degrees per day)</td></tr>
<tr><td>93&ndash;103</td><td>f11.7</td><td>Semimajor axis (AU)</td></tr>
<tr><td>106</td><td>i1 or a1</td><td><a href="uncertainty-parameter.md">Uncertainty parameter</a>, <em>U</em>. Special values: &lsquo;E&rsquo; = assumed eccentricity; &lsquo;D&rsquo; = double designation; &lsquo;F&rsquo; = e-assumed double designation</td></tr>
<tr><td>108&ndash;116</td><td>a9</td><td>Reference</td></tr>
<tr><td>118&ndash;122</td><td>i5</td><td>Number of observations</td></tr>
<tr><td>124&ndash;126</td><td>i3</td><td>Number of oppositions</td></tr>
</tbody>
</table>

---

## Arc Length and Year Span

### Multiple-Opposition Orbits

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>128&ndash;131</td><td>i4</td><td>Year of first observation</td></tr>
<tr><td>132</td><td>a1</td><td>&lsquo;-&rsquo;</td></tr>
<tr><td>133&ndash;136</td><td>i4</td><td>Year of last observation</td></tr>
</tbody>
</table>

### Single-Opposition Orbits

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>128&ndash;131</td><td>i4</td><td>Arc length (days)</td></tr>
<tr><td>133&ndash;136</td><td>a4</td><td>&lsquo;days&rsquo;</td></tr>
</tbody>
</table>

---

## Additional Fields

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>138&ndash;141</td><td>f4.2</td><td>R.m.s residual (&Prime;)</td></tr>
<tr><td>143&ndash;145</td><td>a3</td><td>Coarse indicator of perturbers (blank if unperturbed one-opposition object)</td></tr>
<tr><td>147&ndash;149</td><td>a3</td><td>Precise indicator of perturbers (blank if unperturbed one-opposition object)</td></tr>
<tr><td>151&ndash;160</td><td>a10</td><td>Computer name</td></tr>
</tbody>
</table>

---

## Extended Information (Beyond Column 160)

### Hexdigit Flags (Columns 162--165)

Format: `z4.4` (4-hexdigit flags).

The bottom 6 bits (bits 0--5) encode an orbit type:

| Value | Classification |
|-------|----------------|
| 1     | Atira          |
| 2     | Aten           |
| 3     | Apollo         |
| 4     | Amor           |
| 5     | Object with q < 1.665 AU |
| 6     | Hungaria       |
| 7     | Unused or internal MPC use only |
| 8     | Hilda          |
| 9     | Jupiter Trojan |
| 10    | Distant object |

Additional bit flags convey further information:

| Bit | Value  | Meaning |
|-----|--------|---------|
| 11  | 2048   | Object is NEO |
| 12  | 4096   | Object is 1-km (or larger) NEO |
| 13  | 8192   | 1-opposition object seen at earlier opposition |
| 14  | 16384  | Critical list numbered object |
| 15  | 32768  | Object is PHA |

### Final Columns

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>167&ndash;194</td><td>a</td><td>Readable designation</td></tr>
<tr><td>195&ndash;202</td><td>i8</td><td>Date of last observation included in orbit solution (YYYYMMDD format)</td></tr>
</tbody>
</table>

---

## Notes

- Orbit classification is based on cuts in osculating element space and is not
  100% reliable.
- Certain flags (bits 6--10) are designated for internal MPC use and remain
  undocumented.
