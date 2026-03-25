# Export Format for Comet Orbits

This page describes the formats used for the export version of comet orbits, as used in
the Extended Computer Service and in the Ephemerides and Orbital Elements publications.
Orbital elements for comets are heliocentric.

---

## Extended Computer Service (ECS) Format

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>1&ndash;4</td><td>i4</td><td>Periodic comet number</td></tr>
<tr><td>5</td><td>a1</td><td>Orbit type (generally &lsquo;C&rsquo;, &lsquo;P&rsquo; or &lsquo;D&rsquo;)</td></tr>
<tr><td>6&ndash;12</td><td>a7</td><td>Provisional designation (<a href="../designations/packed-designations.md">packed form</a>)</td></tr>
<tr><td>21&ndash;24</td><td>i4</td><td>Year of perihelion passage</td></tr>
<tr><td>26&ndash;29</td><td>a5</td><td>Month of perihelion passage</td></tr>
<tr><td>30&ndash;37</td><td>f7.4</td><td>Day of perihelion passage (TT)</td></tr>
<tr><td>39&ndash;47</td><td>f9.6</td><td>Perihelion distance (AU)</td></tr>
<tr><td>50&ndash;57</td><td>f8.6</td><td>Orbital eccentricity</td></tr>
<tr><td>59&ndash;63</td><td>f5.2</td><td>Orbital period (years), if &lt; 100</td></tr>
<tr><td>60&ndash;62</td><td>i3</td><td>Orbital period (years), if &ge; 100</td></tr>
<tr><td>66&ndash;73</td><td>f8.4</td><td>Argument of perihelion, J2000.0 (degrees)</td></tr>
<tr><td>76&ndash;83</td><td>f8.4</td><td>Longitude of ascending node, J2000.0 (degrees)</td></tr>
<tr><td>86&ndash;93</td><td>f8.4</td><td>Inclination to ecliptic, J2000.0 (degrees)</td></tr>
<tr><td>96&ndash;97</td><td>i2</td><td>Last two digits of epoch year</td></tr>
<tr><td>99&ndash;103</td><td>a5</td><td>Month of epoch</td></tr>
<tr><td>104&ndash;105</td><td>i2</td><td>Day of epoch (assumed .0 TT)</td></tr>
<tr><td>96&ndash;105</td><td>&mdash;</td><td>Blank if no epoch</td></tr>
<tr><td>107&ndash;111</td><td>i5</td><td>Number of observations in solution</td></tr>
<tr><td>112</td><td>a1</td><td>&lsquo;*&rsquo; indicates non-gravitational parameters considered</td></tr>
<tr><td>114&ndash;118</td><td>a5</td><td>Date of first observation (<a href="../designations/packed-dates.md">packed format</a>)</td></tr>
<tr><td>120&ndash;124</td><td>a5</td><td>Date of last observation (<a href="../designations/packed-dates.md">packed format</a>)</td></tr>
<tr><td>126</td><td>a1</td><td>Source of perturbing coordinates</td></tr>
<tr><td>128&ndash;130</td><td>a3</td><td>Brief descriptor of perturbers (blank if unperturbed)</td></tr>
<tr><td>132&ndash;135</td><td>h4</td><td>Fuller description of perturbers (&lsquo;0000&rsquo; if unperturbed)</td></tr>
<tr><td>137</td><td>i1</td><td>Number of perturbing planets (&lsquo;0&rsquo; unperturbed, &lsquo;9&rsquo; perturbed)</td></tr>
<tr><td>143&ndash;172</td><td>a30</td><td>Name of comet</td></tr>
<tr><td>173&ndash;181</td><td>a9</td><td>Reference</td></tr>
</tbody>
</table>

There is no ambiguity in the century part of the epoch, as the epoch will be
within +/- 20 days of the time of perihelion passage.

---

## Ephemerides and Orbital Elements Format

<table>
<thead>
<tr><th>Columns</th><th>F77</th><th>Use</th></tr>
</thead>
<tbody>
<tr><td>1&ndash;4</td><td>i4</td><td>Periodic comet number</td></tr>
<tr><td>5</td><td>a1</td><td>Orbit type (generally &lsquo;C&rsquo;, &lsquo;P&rsquo; or &lsquo;D&rsquo;)</td></tr>
<tr><td>6&ndash;12</td><td>a7</td><td>Provisional designation (<a href="../designations/packed-designations.md">packed form</a>)</td></tr>
<tr><td>15&ndash;18</td><td>i4</td><td>Year of perihelion passage</td></tr>
<tr><td>20&ndash;21</td><td>i2</td><td>Month of perihelion passage</td></tr>
<tr><td>23&ndash;29</td><td>f7.4</td><td>Day of perihelion passage (TT)</td></tr>
<tr><td>31&ndash;39</td><td>f9.6</td><td>Perihelion distance (AU)</td></tr>
<tr><td>42&ndash;49</td><td>f8.6</td><td>Orbital eccentricity</td></tr>
<tr><td>52&ndash;59</td><td>f8.4</td><td>Argument of perihelion, J2000.0 (degrees)</td></tr>
<tr><td>62&ndash;69</td><td>f8.4</td><td>Longitude of ascending node, J2000.0 (degrees)</td></tr>
<tr><td>72&ndash;79</td><td>f8.4</td><td>Inclination, J2000.0 (degrees)</td></tr>
<tr><td>82&ndash;85</td><td>i4</td><td>Year of epoch (perturbed solutions)</td></tr>
<tr><td>86&ndash;87</td><td>i2</td><td>Month of epoch (perturbed solutions)</td></tr>
<tr><td>88&ndash;89</td><td>i2</td><td>Day of epoch (perturbed solutions)</td></tr>
<tr><td>92&ndash;95</td><td>f4.1</td><td>Absolute magnitude</td></tr>
<tr><td>97&ndash;100</td><td>f4.0</td><td>Slope parameter</td></tr>
<tr><td>103&ndash;158</td><td>a56</td><td>Designation and Name</td></tr>
<tr><td>160&ndash;168</td><td>a9</td><td>Reference</td></tr>
</tbody>
</table>
