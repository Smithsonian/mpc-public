# Digest2 algorithm outline

1.  For each object, the program computes a motion vector from the
available observations, and computes a V magnitude from whatever
photometry is provided, defaulting to 21 if there is no photometry at all.

2.  It then generates a number of orbits that are consistent with
the computed motion, complete with absolute magnitudes consistent with
the computed V magnitude.

3.  Each orbit is located within a binned, or histogram, model of the
Solar System.  The model is binned in the four dimensions of q, e, i, and H.
As the bin is determined for each orbit, a tag is set for that bin.
Additionally, each orbit is tested for each configured class and a separate
tag is set, by bin, for each class.

4.  A search algorithm is used to generate orbits covering the entire range
of possible orbits, and tag corresponding possible bins.  As the algorithm
generates variant orbits, it checks if the orbits are yielding new bin
taggings, either in general or of specific orbit classes.  The algorithm
terminates after reaching a point of diminishing returns in finding bins.

5.  The histogram contains object population counts by bin.  For each bin
there is a population of each orbit class, and also a complete population
count.  After orbit search, the sum of complete population of tagged bins
represents the number of possible candidate objects in the Solar System.
The population sum of tagged bins of a specified class represents the number
of possible candidates of that class.  The class sum divided by the complete
sum represents the fraction of candidate objects that are of that class.
This fraction is multiplied by 100 and output as the "raw" percentage.

6.  No-ID scores are computed similarly with a parallel histogram.
In it, population counts are not of the expected complete population of the
Solar System, but of the expected yet-undiscovered population.  This
population is computed by reducing the modeled complete population by known
discoveries.  As the intended context of the no-ID score is after attempted
object identification, the selected known population is that which is readily
identifiable.  The current criteria used is sky uncertainty < 1' arc.
The uncertainty parameter selected for this comparison is field 24 of
astorb.dat, which is a peak ephemeris uncertainty over a 10 year period.
